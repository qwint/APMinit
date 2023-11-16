import asyncio
import logging
import typing
from NetUtils import JSONtoTextParser, JSONMessagePart, ClientStatus
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger, get_base_parser,
    server_loop,
    ClientCommandProcessor
)
import json
import time
import os
import bsdiff4
from aiohttp import web
# from .proxyFlask import app
import Utils
import settings
from .Items import item_table
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext
    # logger.info("please install the universal tracker :)")

logger = logging.getLogger("Client")

DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111
my_locations = []
for item_name, item_data in item_table.items():
    my_locations.append(item_data.code)


def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)


class ProxyGameJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text


class MinitCommandProcessor(ClientCommandProcessor):

    def _cmd_patch(self):
        """Patch the game."""
        try:
            if isinstance(self.ctx, ProxyGameContext):
                self.ctx.patch_game()
                self.output("Patched.")
        except FileNotFoundError:
            logger.info("Patch cancelled")
        except ValueError:
            logger.info("Selected game is not vanilla, \
                please reset the game and repatch")

    def _cmd_amnisty(self, total: int = 1):
        """Set the Death Amnisty value. Default 1."""
        self.ctx.death_amnisty_total = int(total)
        self.ctx.death_amnisty_count = 0
        logger.info(f"Amnisty set to {self.ctx.death_amnisty_total}. \
            Deaths towards Amnisty reset.")


class RomFile(settings.UserFilePath):
    description = "Minit Vanilla File"
    md5s = [
        "cd676b395dc2a25df10a569c17226dde",
        "1432716643381ced3ad0195078e8e314",
        ]
    # the hashes for vanilla to be verified by the /patch command


class ProxyGameContext(SuperContext):
    game = GAMENAME
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    command_processor = MinitCommandProcessor
    tags = {"AP", "DeathLink"}
    last_sent_death: float = time.time()
    death_amnisty_total: int
    death_amnisty_count: int

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gamejsontotext = ProxyGameJSONToTextParser(self)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []
        self.death_amnisty_total = 1
        self.death_amnisty_count = 0

    def run_gui(self):

        from kvui import GameManager
        logger.info("please install the universal tracker :)")

        class ProxyManager(GameManager):
            # super().__init__()
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Minit Client"

            def build(self):
                container = super().build()
                if tracker_loaded:
                    self.ctx.build_gui(self)

                return container

        self.ui = ProxyManager(self)
        if tracker_loaded:
            self.load_kv()

        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def patch_game(self):
        validator = RomFile()

        source_data_win = Utils.open_filename(
            'Select Minit data.win',
            (('data.win', ('.win',)),))
        validator.validate(source_data_win)
        with open(os.path.join(source_data_win), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), data_path("patch.bsdiff"))
        with open(os.path.join(source_data_win), "wb") as f:
            f.write(patchedFile)
        logger.info(
            "patched " +
            source_data_win +
            ". You can launch the .exe game to run the patched game.")

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == 'Connected':
            Utils.async_start(self.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.missing_locations),
                "create_as_hint": 0
                }]))
        # if cmd == 'ReceivedItems':
        #     #TODO make this actually send minit a ping
        #      - or check if it can be handled with ctx.watcher_event instead
        #     logger.info("send minit a ping")

    async def send_death(self, death_text: str = ""):
        self.death_amnisty_count += 1
        if self.death_amnisty_count == self.death_amnisty_total:
            await super().send_death(death_text)
            self.last_sent_death = time.time()
            self.death_amnisty_count = 0

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ProxyGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    async def locationHandler(self, requestjson: json) -> json:
        """handle POST at /Locations that uses scouts to return useful info"""
        # requestjson = await request.json()
        response = handleLocations(self, requestjson)
        # localResponse = handleLocalLocations(self, requestjson)
        await self.send_msgs(response)
        return handleLocalLocations(self, requestjson)

    async def goalHandler(self) -> json:
        """handle POST at /Goal"""
        response = handleGoal(self)
        await self.send_msgs(response)
        return response

    async def deathHandler(self) -> json:
        """handle POST at /Death"""
        response = handleDeathlink(self)
        await self.send_death("ran out of time")
        return response

    async def deathpollHandler(self) -> json:
        """handle GET at /Deathpoll"""
        cTime = 0
        while (cTime < 20):
            if self.last_death_link > self.last_sent_death:
                self.last_sent_death = self.last_death_link
                return json({"Deathlink": True})
            else:
                cTime += 1
                await asyncio.sleep(1)
        return json({"Deathlink": False})

    async def itemsHandler(self) -> json:
        """handle GET at /Items"""
        # response = handleItems(self)
        return handleItems(self)

    async def datapackageHandler(self) -> json:
        """handle GET at /Datapackage"""
        # response = handleDatapackage(self)
        # response = {'datapackage':'FROM MINIT - need to figure out data'}
        # await self.send_msgs(response)
        return handleDatapackage(self)

    # async def locationHandler(self, request: web.Request) -> web.Response:
    #     ""handle POST at /Locations that uses scouts to return useful info"""
    #     requestjson = await request.json()
    #     response = handleLocations(self, requestjson)
    #     localResponse = handleLocalLocations(self, requestjson)
    #     await self.send_msgs(response)
    #     return web.json_response(localResponse)

    # async def goalHandler(self, request: web.Request) -> web.Response:
    #     """handle POST at /Goal"""
    #     response = handleGoal(self)
    #     await self.send_msgs(response)
    #     return web.json_response(response)

    # async def deathHandler(self, request: web.Request) -> web.Response:
    #     """handle POST at /Death"""
    #     response = handleDeathlink(self)
    #     await self.send_death("ran out of time")
    #     return web.json_response(response)

    # async def deathpollHandler(self, request: web.Request) -> web.Response:
    #     """handle GET at /Deathpoll"""
    #     cTime = 0
    #     while (cTime < 20):
    #         if self.last_death_link > self.last_sent_death:
    #             self.last_sent_death = self.last_death_link
    #             return web.json_response({"Deathlink": True})
    #         else:
    #             cTime += 1
    #             await asyncio.sleep(1)
    #     return web.json_response({"Deathlink": False})

    # async def itemsHandler(self, request: web.Request) -> web.Response:
    #     """handle GET at /Items"""
    #     response = handleItems(self)
    #     return web.json_response(response)

    # async def datapackageHandler(self, request: web.Request) -> web.Response:
    #     """handle GET at /Datapackage"""
    #     response = handleDatapackage(self)
    #     # response = {'datapackage':'FROM MINIT - need to figure out data'}
    #     # await self.send_msgs(response)
    #     return web.json_response(response)


def handleDeathlink(ctx: CommonContext) -> json:
    deathlinkmessage = "death sent"
    return deathlinkmessage


def handleGoal(ctx: CommonContext) -> json:
    goalmessage = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
    return goalmessage


def handleLocations(ctx: CommonContext, request: json) -> json:
    # expecting request to be json body in the form of {"Locations": [123,456]}

    # TODO - make this actually send the difference
    needed_updates = set(request["Locations"]).difference(
        ctx.locations_checked)
    locationmessage = [{
        "cmd": "LocationChecks",
        "locations": list(needed_updates)
        }]
    return locationmessage


def handleLocalLocations(ctx: CommonContext, request: json) -> json:
    # expecting request to be json body in the form of
    # {"LocationResponse":
    #     {"Player": "qwint", "Item": "ItemGrinder", "Code": 60017}
    # - for a local item
    # {"LocationResponse": {"Player": "OtherPlayer", "Item": "ItemGrinder"}
    # - for a remote item

    # TODO - make this not break if the sent item is not in missing locations
    # - (the things we scouted for)
    # TODO - make the game mod not crash if something doesn't have
    # - an item value after translate
    # TODO - load the datapackage so i can get translated names
    # - instead of setting their ids to strings
    # TODO - still find a way to make the scouts launch automatically

    locations = set(request["Locations"]).difference(ctx.locations_checked)
    if len(locations) == 1:
        location = request["Locations"][0]
        if (len(ctx.locations_info) > 0):
            if location in ctx.locations_info:
                loc = ctx.locations_info[location]
                slot = loc.player
                player = ctx.slot_info[loc.player].name
                item = ctx.item_names[loc.item]
                code = loc.item

                if ctx.slot_concerns_self(slot):
                    locationmessage = {
                        "Player": player,
                        "Item": item,
                        "Code": code}
                else:
                    locationmessage = {"Player": player, "Item": item}
                return locationmessage
            # else:
                # logger.info("location not found in the scouts")
                # not found in the scouts that do exist
        # else:
            # logger.info("no scouts found to hint names for location pickup")
    # else:
        # logger.info("len(Locations) == 1 resolved to false")
        # error handle

    # if we couldn't handle the logic send back benign message
    return {"Location": "Not found in scout cache"}


def handleItems(ctx: CommonContext) -> json:
    # expecting request to be json body in the form of
    # {"Items": [123,456],"Coins":2, "Hearts": 1, "Tentacles":4}
    itemIds = []
    coins = 0
    hearts = 0
    tentacles = 0
    for item in ctx.items_received:
        if item[0] == 60000:
            coins += 1
        elif item[0] == 60001:
            hearts += 1
        elif item[0] == 60002:
            tentacles += 1
        else:
            itemIds.append(item[0])
    itemmessage = {
        "Items": itemIds,
        "Coins": coins,
        "Hearts": hearts,
        "Tentacles": tentacles
    }
    return itemmessage


# TODO update to transform the data
# - will eventually handle the datapackage from
# - CommonContext.consume_network_data_package() to make them minit pretty
def handleDatapackage(ctx: CommonContext) -> json:
    datapackagemessage = [{"cmd": "blah", "data": "blah"}]
    return datapackagemessage


async def main(args):
    # from .proxyServer import Webserver, http_server_loop
    from .proxyQuart import quartContext, http_server_loop
    ctx = ProxyGameContext(args.connect, args.password)
    # webserver = Webserver(ctx)
    appCtx = quartContext(ctx)

    ctx.httpServer_task = asyncio.create_task(
        appCtx.my_run_app(),
        name="http server loop"
        )

    # httpServer_thread = threading.Thread(
    #     target=asyncio.new_event_loop().run_forever,
    #     name="http server loop"
    #     )
    # httpServer_thread.start()

    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(
        server_loop(ctx),
        name="server loop"
        )

    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    import colorama

    parser = get_base_parser(
        description="Gameless Archipelago Client, for text interfacing."
        )
    parser.add_argument(
        '--name',
        default=None,
        help="Slot Name to connect as."
        )
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()
