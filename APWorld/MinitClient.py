import asyncio
import logging
import typing
from NetUtils import JSONtoTextParser, JSONMessagePart, ClientStatus
from CommonClient import CommonContext, gui_enabled, logger, get_base_parser, server_loop, ClientCommandProcessor
#probably need
#import urllib.parse
#webserver imports
import json
import os
import bsdiff4
from aiohttp import web
import Utils

logger = logging.getLogger("Client")

DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111

def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)

#parsing function
class ProxyGameJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text


class MinitCommandProcessor(ClientCommandProcessor):
    # def __init__(self, ctx):
    #     super().__init__()
    #     self.ctx = ctx

    def _cmd_patch(self):
        """Patch the game."""
        try:
            if isinstance(self.ctx, ProxyGameContext):
                #os.makedirs(name=os.path.join(os.getcwd(), "Minit"), exist_ok=True)
                self.ctx.patch_game()
                self.output("Patched.")
        except FileNotFoundError:
            logger.info("Patch cancelled")


#TODO look into how this can be handled as a ctx.watcher_event instead
# #this should work to intercept the process server command method, let it run as written, but then also handle received items to 'send a ping' to the game (as of now a log message isntead)
# async def process_server_cmd(ctx: CommonContext, args: dict):
#     super(ctx, args)
#     try:
#         cmd = args["cmd"]
#     except:
#         logger.exception(f"Could not get command from {args}")
#         raise
#     if cmd == 'ReceivedItems':
#         #TODO make this actually send minit a ping
#         logger.info("send minit a ping")

class ProxyGameContext(CommonContext):
    game = GAMENAME
    httpServer_task: typing.Optional["asyncio.Task[None]"] = None
    command_processor = MinitCommandProcessor

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gamejsontotext = ProxyGameJSONToTextParser(self)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []

    def run_gui(self):
        from kvui import GameManager

        class UTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Minit Client"

        self.ui = UTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def patch_game(self):
        source_data_win = Utils.open_filename('Select Minit data.win', (('data.win', ('.win',)),))
        with open(os.path.join(source_data_win), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), data_path("patch.bsdiff"))
        with open(os.path.join(source_data_win), "wb") as f:
            f.write(patchedFile)
        logger.info("patched "+source_data_win+". You can launch the .exe game to run the patched game.")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ProxyGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    #handle POST at /Locations
    async def locationHandler(self, request: web.Request) -> web.Response:
        response = handleLocations(self, await request.json())
        await self.send_msgs(response)
        return web.json_response(str(response)) 
    #handle POST at /Goal
    async def goalHandler(self, request: web.Request) -> web.Response:
        response = handleGoal(self)
        await self.send_msgs(response)
        return web.json_response(response) 
    #handle GET at /Items
    async def itemsHandler(self, request: web.Request) -> web.Response:
        #response = handleItems(ctx)
        response = handleItems(self)
        #response = {'items':[123,456]}
        #await self.send_msgs(response)
        return web.json_response(response) 
    #handle GET at /Datapackage
    async def datapackageHandler(self, request: web.Request) -> web.Response:
        #response = handleDatapackage(ctx)
        response = handleDatapackage(self)
        #response = {'datapackage':'FROM MINIT - need to figure out data'}
        #await self.send_msgs(response)
        return web.json_response(response) 

def handleGoal(ctx: CommonContext):
    goalmessage = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
    return goalmessage

def handleLocations(ctx: CommonContext, request: json) -> json:
    #expecting request to be json body in the form of {"Locations": [123,456]}
    #TODO - make this actually send the difference
    needed_updates = set(request["Locations"]).difference(ctx.locations_checked)
    locationmessage = [{"cmd": "LocationChecks", "locations": list(needed_updates)}]
    #TODO - (see if i need to) handle locationId -1 receivedItems (from a /send or !get)
    return locationmessage

def handleItems(ctx: CommonContext):
    #expecting request to be json body in the form of {"Items": [123,456],"Coins":2, "Hearts": 1, "Tentacles":4}
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
    itemmessage = {"Items": itemIds,"Coins":coins, "Hearts": hearts, "Tentacles":tentacles}
    #itemmessage = {"Items": [{"first": 60018},{"second":  60007},{"third":  60008}], "Coins": 2, "Hearts": 0, "Tentacles": 0}
    return itemmessage

#TODO update to transform the data - will eventually handle the datapackage from CommonContext.consume_network_data_package() to make them minit pretty
def handleDatapackage(ctx: CommonContext):
    datapackagemessage = [{"cmd": "blah", "data": "blah"}]
    return datapackagemessage

async def main(args):
    from .testServer import Webserver, http_server_loop
    
    ctx = ProxyGameContext(args.connect, args.password)
    webserver = Webserver(ctx)
    ctx.httpServer_task = asyncio.create_task(http_server_loop(webserver), name="http server loop")

    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()

def launch():
    import colorama

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
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
