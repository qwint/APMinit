import asyncio
import logging
from NetUtils import JSONtoTextParser, JSONMessagePart
from CommonClient import CommonContext, gui_enabled, logger, get_base_parser, server_loop


logger = logging.getLogger("Client")

DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111

#parsing function
class ProxyGameJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text

#this should work to intercept the process server command method, let it run as written, but then also handle received items to 'send a ping' to the game (as of now a log message isntead)
async def process_server_cmd(ctx: CommonContext, args: dict):
    super(ctx, args)
    try:
        cmd = args["cmd"]
    except:
        logger.exception(f"Could not get command from {args}")
        raise
    if cmd == 'ReceivedItems':
        #TODO make this actually send minit a ping
        logger.info("send minit a ping")

class ProxyGameContext(CommonContext):
    game = GAMENAME

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

#potential steal of datapackage code to handle minit specific translations if needed 
#    def consume_network_data_package(self, data_package: dict):
#        super(data_package['data'])

#TODO update to use proper python - barebones handle logic for requests from Minit
def handle_POST(self, ctx: CommonContext):
    if request.path == "Location"
        send_server_cmd('LocationChecks', ['locations',handleLocations(ctx)])
    elif request.path == "Goal"
        send_server_cmd('StatusUpdate',['status':'CLIENT_GOAL'])    
def handle_GET(self, ctx: CommonContext):
    if request.path == "Items"
        response = handleItems(ctx)
    elif request.path == "Datapackage"
        response = handleDatapackage(ctx)

#TODO update to transform the data - will eventually handle the data from minit to format them for LocationChecks API call
def handleLocations(ctx: CommonContext):
    return ctx.locations_checked
    # return [123,456] where 123 and 456 are all of the locations that minit has reported checked

#TODO update to transform the data - will eventually handle the items_received to make them minit pretty
def handleItems(ctx: CommonContext):
    return ctx.items_received

#TODO update to transform the data - will eventually handle the datapackage from CommonContext.consume_network_data_package() to make them minit pretty
def handleDatapackage(ctx: CommonContext):
    return ctx.datapackage

async def main(args):
    ctx = ProxyGameContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    #TODO host an HTTP server that waits for requests and uses handle_POST() and handle_GET()

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
