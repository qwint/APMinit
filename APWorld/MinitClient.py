import asyncio
import logging
import typing
from NetUtils import JSONtoTextParser, JSONMessagePart
from CommonClient import CommonContext, gui_enabled, logger, get_base_parser, server_loop


#webserver imports
import json
from uuid import uuid4
from aiohttp import web
#from aiopg.sa import create_engine

logger = logging.getLogger("Client")

DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111

#parsing function
class ProxyGameJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text

# class Webserver:
#     def __init__(self):#, **kwargs: dict):
#         self.app = web.Application()
#         self.host = "localhost"#kwargs['webserver']['host']
#         self.port = "11311"#kwargs['webserver']['port']
#         #self.dbconf = kwargs['db']
#         self.sessionToUser = {}
#         self.userToSession = {}

#     async def initializer(self) -> web.Application:
#         # self.dbEngine = await create_engine(
#         #     user = self.dbConf['user'],
#         #     password = self.dbConf['password'],
#         #     host = self.dbConf['host'],
#         #     database = self.dbConf['database'],
#         #     )
#         self.app.router.add_post('/user',self.loginHandler)
#         self.app.router.add_delete('/user',self.loginHandler)
#         return self.app

#     async def loginHandler(self, request: web.Request) -> web.Response:
#         response = {'hello world': 0}
#         return web.json_response(response)

#     def run(self):
#         web.run_app(self.initializer(),host=self.host, port=self.port)


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

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gamejsontotext = ProxyGameJSONToTextParser(self)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ProxyGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def locationHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
        #send_server_cmd('LocationChecks', ['locations',handleLocations(ctx)])
        response = {'locations':[123,456]}
        return web.json_response(response)
    def goalHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
        #send_server_cmd('StatusUpdate',['status':'CLIENT_GOAL'])   
        response = {'status':'GOAL_COMPLETE'}
        return web.json_response(response) 
    def itemsHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
        #response = handleItems(ctx)
        response = {'items':[123,456]}
        return web.json_response(response)
    def datapackageHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
        #response = handleDatapackage(ctx)
        response = {'datapackage':'FROM MINIT - need to figure out data'}
        return web.json_response(response)

#potential steal of datapackage code to handle minit specific translations if needed 
#    def consume_network_data_package(self, data_package: dict):
#        super(data_package['data'])

#TODO update to use proper python - barebones handle logic for requests from Minit
# def handle_POST(self, ctx: CommonContext):
#     if request.path == "Location":
#         send_server_cmd('LocationChecks', ['locations',handleLocations(ctx)])
#     elif request.path == "Goal":
#         send_server_cmd('StatusUpdate',['status':'CLIENT_GOAL'])    
# def handle_GET(self, ctx: CommonContext):
#     if request.path == "Items":
#         response = handleItems(ctx)
#     elif request.path == "Datapackage":
#         response = handleDatapackage(ctx)

#TODO update to transform the data - will eventually handle the data from minit to format them for LocationChecks API call
def handleLocations(ctx: CommonContext):
    #TODO - handle locationId -1 receivedItems (from a /send or !get)
    #TODO pair locations down to just those 
    return ctx.locations_checked
    # return [123,456] where 123 and 456 are all of the locations that minit has reported checked

#TODO update to transform the data - will eventually handle the items_received to make them minit pretty
def handleItems(ctx: CommonContext):
    #TODO add items from cache if needed
    return ctx.items_received

#TODO update to transform the data - will eventually handle the datapackage from CommonContext.consume_network_data_package() to make them minit pretty
def handleDatapackage(ctx: CommonContext):
    return ctx.datapackage

async def main(args):
    from .testServer import Webserver, http_server_loop
    
    ctx = ProxyGameContext(args.connect, args.password)
    webserver = Webserver(ctx)
    ctx.server_task = asyncio.create_task(http_server_loop(webserver), name="http server loop")

    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    #TODO host an HTTP server that waits for requests and uses handle_POST() and handle_GET()

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()

# async def httpMain(args):
#     from .testServer import Webserver, http_server_loop
    
#     ctx = ProxyGameContext(args.connect, args.password)
#     webserver = Webserver(ctx)
#     ctx.server_task = asyncio.create_task(http_server_loop(webserver), name="http server loop")


#     await ctx.exit_event.wait()
#     await ctx.shutdown()

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

    # asyncio.run(httpMain(args))
    # logger.info("httpMain kicked off")
    asyncio.run(main(args))
    colorama.deinit()
