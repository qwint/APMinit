import asyncio
import typing
from NetUtils import ClientStatus, RawJSONtoTextParser
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    get_base_parser,
    server_loop,
    ClientCommandProcessor
)
import json
from typing import List
import time
import os
import bsdiff4
from aiohttp import web
import Utils
import settings
from .Items import item_table
from .ERData import er_entrances, game_entrances
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext


DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111


def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)


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
            logger.info("Selected game is not vanilla, please reset the game and repatch")

    def _cmd_amnisty(self, total: int = 1):
        """Set the Death Amnisty value. Default 1."""
        self.ctx.death_amnisty_total = int(total)
        self.ctx.death_amnisty_count = 0
        logger.info(f"Amnisty set to {self.ctx.death_amnisty_total}. \
            Deaths towards Amnisty reset.")


class RomFile(settings.UserFilePath):
    description = "Minit Vanilla File"
    md5s = [
        "cd676b395dc2a25df10a569c17226dde", #steam
        "1432716643381ced3ad0195078e8e314", #epic
        # "6263766b38038911efff98423822890e", #itch.io, does not work
        ]
    # the hashes for vanilla to be verified by the /patch command


class ProxyGameContext(SuperContext):
    game = GAMENAME
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    command_processor = MinitCommandProcessor
    tags = {"DeathLink"}
    last_sent_death: float = time.time()
    slot_data: dict[str, any]
    death_amnisty_total: int
    death_amnisty_count: int
    goals: List[str]

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gamejsontotext = RawJSONtoTextParser(self)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []
        self.death_amnisty_total = 1  # should be rewritten by slot data
        self.death_amnisty_count = 0

    def run_gui(self):

        from kvui import GameManager

        class ProxyManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Minit Client"

            def build(self):
                container = super().build()
                if tracker_loaded:
                    self.ctx.build_gui(self)
                else:
                    logger.info("to enable a tracker, install Universal Tracker")

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
            self.slot_data = args["slot_data"]
            self.death_amnisty_total = self.slot_data["death_amnisty_total"]
            # if load(ctx.locations_info):
            #     load(ctx.locations_info)
            # else:
            Utils.async_start(self.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.missing_locations),
                "create_as_hint": 0
                }]))
            self.goals = self.slot_data["goals"]
        # if cmd == 'LocationInfo':
        #     save(ctx.locations_info)
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

    async def locationHandler(self, request: web.Request) -> web.Response:
        """handle POST at /Locations that uses scouts to return useful info"""
        requestjson = await request.json()
        response = handleLocations(self, requestjson)
        localResponse = handleLocalLocations(self, requestjson)
        await self.send_msgs(response)
        return web.json_response(localResponse)

    async def goalHandler(self, request: web.Request) -> web.Response:
        """handle POST at /Goal"""
        requestjson = await request.text()
        response = handleGoal(self, requestjson)
        if response:
            await self.send_msgs(response)
        return web.json_response(response)

    async def deathHandler(self, request: web.Request) -> web.Response:
        """handle POST at /Death"""
        if self.slot_data["death_link"]:
            response = handleDeathlink(self)
            await self.send_death("ran out of time")
            return web.json_response(response)
        else:
            return web.json_response("deathlink disabled")

    async def deathpollHandler(self, request: web.Request) -> web.Response:
        """handle GET at /Deathpoll"""
        if self.slot_data["death_link"]:
            cTime = 0
            while (cTime < 20):
                if self.last_death_link > self.last_sent_death:
                    self.last_sent_death = self.last_death_link
                    return web.json_response({"Deathlink": True})
                else:
                    cTime += 1
                    await asyncio.sleep(1)
            return web.json_response({"Deathlink": False})
        else:
            return web.json_response("deathlink disabled")

    async def itemsHandler(self, request: web.Request) -> web.Response:
        """handle GET at /Items"""
        response = handleItems(self)
        return web.json_response(response)

    async def datapackageHandler(self, request: web.Request) -> web.Response:
        """handle GET at /Datapackage"""
        response = handleDatapackage(self)
        # response = {'datapackage':'FROM MINIT - need to figure out data'}
        # await self.send_msgs(response)
        return web.json_response(response)

    async def erConnHandler(self, request: web.Request) -> web.Response:
        """handle GET at /ErConnections"""
        response = handleErConnections(self)
        return web.json_response(response)


def handleErConnections(ctx: CommonContext):
    """
    erMessage format:
    {"Entrances": [
        "hom10_10": [
            {
                "direction": "south",
                "baseCoor": 0,
                "offset": 224,
                "out": {
                    "room": "hom10_10",
                    "x": 0,
                    "y": 0,
                }
            },
            {
                "direction": "north",
                "baseCoor": 0,
                "offset": 224,
                "out": {
                    "room": "hom10_10",
                    "x": 0,
                    "y": 0,
                }
            }
        ],
        "rom10_10": [
            {
                "direction": "south",
                "baseCoor": 0,
                "offset": 224,
                "out": {
                    "room": "hom10_10",
                    "x": 0,
                    "y": 0,
                }
            },
            {
                "direction": "door",
                "x": 0,
                "y": 224,
                "out": {
                    "room": "hom10_10",
                    "x": 0,
                    "y": 0,
                }
            }
        ]
    ]}
    """
    connections = ctx.slot_data["ER_connections"]
    erMessage = {"Entrances": game_entrances}
    if connections:
        for connection in connections:
            left = connection[0]
            right = connection[1]
            for e in er_entrances:
                if e.entrance_name == left:
                    left_entrance = e
                if e.entrance_name == right:
                    right_entrance = e

            print(f"left_entrance: {left_entrance}")
            print(f"right_entrance: {right_entrance}")
            left_tile = left_entrance.room_tile
            print(f"left_tile: {left_tile}")
            left_name = left_entrance.entrance_name
            print(f"left_name: {left_name}")

            index = 0
            for entrance in erMessage["Entrances"][left_tile]:
                if left_name == entrance["CName"]:
                    erMessage["Entrances"][left_tile][index]["out"] = {
                        "tile": right_entrance.room_tile,
                        "x": right_entrance.x_cord,
                        "y": right_entrance.y_cord,
                        "offDir": right_entrance.offset_direction,
                        "offNum": right_entrance.offset_value,
                        }
                index += 1

    else:
        erMessage = "ER Disabled"
    return erMessage


def handleDeathlink(ctx: CommonContext):
    deathlinkmessage = "death sent"
    return deathlinkmessage


def handleGoal(ctx: CommonContext, request: str):
    if request in ctx.goals:
        goalmessage = [{
            "cmd": "StatusUpdate",
            "status": ClientStatus.CLIENT_GOAL
            }]
    else:
        goalmessage = None
    return goalmessage


def handleLocations(ctx: CommonContext, request: json) -> json:
    """
    expecting request to be json body in the form of
    {"Locations": [123,456]}
    """

    # TODO - make this actually send the difference
    needed_updates = set(request["Locations"]).difference(
        ctx.locations_checked)
    locationmessage = [{
        "cmd": "LocationChecks",
        "locations": list(needed_updates)
        }]
    return locationmessage


def handleLocalLocations(ctx: CommonContext, request: json) -> json:
    """
    expecting request to be json body in the form of
    {"LocationResponse":
        {"Player": "qwint", "Item": "ItemGrinder", "Code": 60017}
    - for a local item
    {"LocationResponse": {"Player": "OtherPlayer", "Item": "ItemGrinder"}
    - for a remote item
    """

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
    return {"Location": "Not found in scout cache"}


def handleItems(ctx: CommonContext):
    """
    expecting request to be json body in the form of
    {"Items": [123,456],"Coins":2, "Hearts": 1, "Tentacles":4}
    """
    itemIds = []
    coins = 0
    hearts = 0
    tentacles = 0
    swordsF = 0
    swordsR = 0
    for item in ctx.items_received:
        # TODO - change to lookup ids for actual item names
        if item[0] == 60000:
            coins += 1
        elif item[0] == 60001:
            hearts += 1
        elif item[0] == 60002:
            tentacles += 1
        elif item[0] == 60021:
            swordsF += 1
        elif item[0] == 60022:
            swordsR += 1
        else:
            itemIds.append(item[0])
    itemmessage = {
        "Items": itemIds,
        "Coins": coins,
        "Hearts": hearts,
        "Tentacles": tentacles,
        "swordsF": swordsF,
        "swordsR": swordsR,
    }
    return itemmessage


# TODO update to transform the data
# - will eventually handle the datapackage from
# - CommonContext.consume_network_data_package() to make them minit pretty
def handleDatapackage(ctx: CommonContext):
    datapackagemessage = [{"cmd": "blah", "data": "blah"}]
    return datapackagemessage


async def main(args):
    from .proxyServer import Webserver, http_server_loop

    ctx = ProxyGameContext(args.connect, args.password)
    webserver = Webserver(ctx)
    ctx.httpServer_task = asyncio.create_task(
        http_server_loop(webserver),
        name="http server loop"
        )

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
        description="Minit Archipelago Client."
        )
    args, unknown = parser.parse_known_args()

    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    launch()
