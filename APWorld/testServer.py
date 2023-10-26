#webserver imports
import asyncio
import json
from uuid import uuid4
from aiohttp import web
#from aiopg.sa import create_engine

from .MinitClient import ProxyGameContext
from CommonClient import CommonContext, logger#, gui_enabled, logger, get_base_parser, server_loop



class Webserver:
    def __init__(self, ctx: ProxyGameContext):#, **kwargs: dict):
        self.app = web.Application()
        self.host = "localhost"#kwargs['webserver']['host']
        self.port = "11311"#kwargs['webserver']['port']
        #self.dbconf = kwargs['db']
        self.sessionToUser = {}
        self.userToSession = {}
        self.ctx = ctx

        self.connected = False

    async def initializer(self) -> web.Application:
        # self.dbEngine = await create_engine(
        #     user = self.dbConf['user'],
        #     password = self.dbConf['password'],
        #     host = self.dbConf['host'],
        #     database = self.dbConf['database'],
        #     )
        self.app.router.add_post('/Location',self.ctx.locationHandler)
        self.app.router.add_post('/Goal',self.ctx.goalHandler)
        self.app.router.add_get('/Items',self.ctx.itemsHandler)
        self.app.router.add_get('/Datapackage',self.ctx.datapackageHandler)
        return self.app
    # def locationHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
    #     #send_server_cmd('LocationChecks', ['locations',handleLocations(ctx)])
    #     response = {'locations':[123,456]}
    #     return web.json_response(response)
    # def goalHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
    #     #send_server_cmd('StatusUpdate',['status':'CLIENT_GOAL'])   
    #     response = {'status':'GOAL_COMPLETE'}
    #     return web.json_response(response) 
    # def itemsHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
    #     #response = handleItems(ctx)
    #     response = {'items':[123,456]}
    #     return web.json_response(response)
    # def datapackageHandler(self, request: web.Request) -> web.Response:#, ctx: CommonContext):
    #     #response = handleDatapackage(ctx)
    #     response = {'datapackage':'need to figure out data'}
    #     return web.json_response(response)

    async def loginHandler(self, request: web.Request) -> web.Response:
        response = {'hello world': 0}
        return web.json_response(response)

    async def my_run_app(self, app, host, port):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

        while True:
            await asyncio.sleep(3600)  # sleep forever

    async def run(self):
        if self.connected != True:
            await self.my_run_app(app=await self.initializer(),host=self.host, port=self.port)
            #web.run_app(self.initializer(),host=self.host, port=self.port)
            self.connected = True
            return self.connected
        else:
            logger.info('Already connected')
            return

async def http_server_loop(wb: Webserver) -> None:
    try:
        logger.info('Trying to launch http server')
        await wb.run()
    finally:
        logger.info('http_server_loop ended')
    # except websockets.InvalidMessage:
    #     # probably encrypted
    #     if address.startswith("ws://"):
    #         # try wss
    #         await server_loop(ctx, "ws" + address[1:])
    #     else:
    #         ctx.handle_connection_loss(f"Lost connection to the multiworld server due to InvalidMessage"
    #                                    f"{reconnect_hint()}")
    # except ConnectionRefusedError:
    #     wb.ctx.handle_connection_loss("Connection refused by the server. "
    #                                "May not be running Archipelago on that address or port.")
    # # except websockets.InvalidURI:
    # #     wb.ctx.handle_connection_loss("Failed to connect to the multiworld server (invalid URI)")
    # except OSError:
    #     wb.ctx.handle_connection_loss("Failed to connect to the multiworld server")
    # except Exception:
    #     wb.ctx.handle_connection_loss(f"Lost connection to the multiworld server{reconnect_hint()}")
    # finally:
    #     await wb.ctx.connection_closed()
    #     if wb.ctx.server_address and wb.ctx.username and not wb.ctx.disconnected_intentionally:
    #         logger.info(f"... automatically reconnecting in {wb.ctx.current_reconnect_delay} seconds")
    #         assert wb.ctx.autoreconnect_task is None
    #         wb.ctx.autoreconnect_task = asyncio.create_task(server_autoreconnect(wb.ctx), name="server auto reconnect")
    #     wb.ctx.current_reconnect_delay *= 2


if __name__ == '__main__':
    ctx = ProxyGameContext("localhost","")

    webserver = Webserver(ctx)
    webserver.run()