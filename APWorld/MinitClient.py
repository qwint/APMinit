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
import settings
#from settings import FilePath
from .Items import item_table

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
        except ValueError:
            logger.info("Selected game is not vanilla, please reset the game and repatch")

    # def _cmd_scout(self):
    #     """manually scouts locations for the fanfares."""
    #     Utils.async_start(self.ctx.send_msgs([{"cmd": "LocationScouts", "locations": list(self.ctx.missing_locations), "create_as_hint":0}]))

    # def _cmd_print(self):
    #     """prints cached values for debugging."""
    #     logger.info("locations info: " + str(self.ctx.locations_info))
    #     logger.info("missing locations: " + str(self.ctx.missing_locations))


class RomFile(settings.UserFilePath):
    description = "Minit Vanilla File"
    md5s = ["cd676b395dc2a25df10a569c17226dde","1432716643381ced3ad0195078e8e314"]
        #the hash for vanilla to be verified by the /patch command


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
        validator = RomFile()


        source_data_win = Utils.open_filename('Select Minit data.win', (('data.win', ('.win',)),))
        validator.validate(source_data_win)
        with open(os.path.join(source_data_win), "rb") as f:
            patchedFile = bsdiff4.patch(f.read(), data_path("patch.bsdiff"))
        with open(os.path.join(source_data_win), "wb") as f:
            f.write(patchedFile)
        logger.info("patched "+source_data_win+". You can launch the .exe game to run the patched game.")

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            Utils.async_start(self.send_msgs([{"cmd": "LocationScouts", "locations": list(self.missing_locations), "create_as_hint":0}]))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ProxyGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    #handle POST at /Locations that utilizes scouts to return useful info if possible
    async def locationHandler(self, request: web.Request) -> web.Response:
        requestjson = await request.json()
        response = handleLocations(self, requestjson)
        localResponse = handleLocalLocations(self, requestjson)
        await self.send_msgs(response)
        return web.json_response(localResponse)
        #return web.json_response({"Player": "qwint", "Item": "ItemMegaSword", "Code": 60014}) 
        #return web.json_response({"Player": "other", "Item": "Swim"}) 
        #return web.json_response({"Location": "Not found in scout cache"})

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
    return locationmessage

def handleLocalLocations(ctx: CommonContext, request: json) -> json:
    #expecting request to be json body in the form of 
    #{"LocationResponse": {"Player": "qwint", "Item": "ItemGrinder", "Code": 60017} for a local item
    #{"LocationResponse": {"Player": "OtherPlayer", "Item": "ItemGrinder"} for a remote item

    #TODO - make this not break if the sent item is not in missing locations (the things we scouted for)
    #TODO - make the game mod not crash if something doesn't have an item value after translate
    #TODO - load the datapackage so i can get translated names instead of setting their ids to strings
    #TODO - still find a way to make the scouts launch automatically

    locations = set(request["Locations"]).difference(ctx.locations_checked)
    if len(locations) == 1:
        location = request["Locations"][0]
        #logger.info("location: "+str(location))

        if (len(ctx.locations_info) > 0):
            #logger.info("trying to handle local locations")
            if location in ctx.locations_info:
                loc = ctx.locations_info[location] #locations_scouted:
               # logger.info("location found in info")
                slot = loc.player #don't convert
                player = ctx.slot_info[loc.player].name #convert to text
                item = ctx.item_names[loc.item] #convert to text
                code = loc.item #don't convert

                if ctx.slot_concerns_self(slot): #confirm this is true if local items
                    locationmessage = {"Player": player, "Item": item, "Code": code}
                else: 
                    locationmessage = {"Player": player, "Item": item}

                #logger.info("message sent: " +str(locationmessage))
                #needed_updates = set(request["Locations"]).difference(ctx.locations_checked)
                #locationmessage = {"Player": "qwint", "Item": "ItemGrinder", "Code": 60017}
                return locationmessage
            #else: 
                #logger.info("location not found in the scouts")
                #not found in the scouts that do exist
        #else: 
            #logger.info("no scouts found to hint names for location pickup")
    #else: 
        #logger.info("len(Locations) == 1 resolved to false")
        #error handle

    #if we couldn't handle the logic send back benign message
    return {"Location": "Not found in scout cache"}
    
        
#on connect somewhere
#ctx.send_msgs([{"cmd": "LocationScouts", "locations": list(my_locations), "create_as_hint":0}])
#potential use ctx.missing_locations instead of my_locations (esp if that doesn't work)

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
