import asyncio
import json
# from uuid import uuid4
# from aiohttp import web
from flask import Flask
from a2wsgi import WSGIMiddleware

# from .MinitClient import ProxyGameContext
logger_loaded = False
try:
    from CommonClient import logger
    logger_loaded = True
except ModuleNotFoundError:
    print("logging with print")


def printLog(str: str):
    if logger_loaded:
        logger.info(str)
    else:
        print(str)


class flaskContext2():
    app = Flask(__name__)

    @app.route("/")
    def index():
        async def _index():
            return await something

        result = asynchio.run(_index())
        return result


class flaskContext():
    # from .MinitClient import ProxyGameContext
    ctx = None  # : ProxyGameContext

    def __init__(self, ctx):
        self.ctx = ctx

    app = Flask(__name__)

    app.config["DEBUG"] = False
    app.config["PORT"] = 11311
    app.config["WAITRESS_THREADS"] = 10
    app.config["HOST_ADDRESS"] = "localhost"
    # ctx = None  # : ProxyGameContext

    @app.route("/Locations", methods=['POST'])
    async def Locations_api():
        return {"Locations": {"one": "value"}}

    @app.route("/Goal", methods=['POST'])
    async def Goal_api():
        return {"Goal": {"one": "value"}}

    @app.route("/Death", methods=['POST'])
    async def Death_api():
        return {"Death": {"one": "value"}}

    @app.route("/Deathpoll", methods=['GET'])
    async def Deathpoll_api():
        return {"Deathpoll": {"one": "value"}}

    @app.route("/Items", methods=['GET'])
    async def Items_api():
        return self.ctx.itemsHandler()
        # return {"Items": {"one": "value"}}

    @app.route("/Datapackage", methods=['GET'])
    async def Datapackage_api():
        return {"Datapackage": {"one": "value"}}

    async def my_run_app(self):
        # from waitress import serve
        # await serve(
        #     app,
        #     port=self.app.config["PORT"],
        #     threads=self.app.config["WAITRESS_THREADS"],
        #     debug=self.app.config["DEBUG"]
        #     )

        # while True:
        #     await asyncio.sleep(3600)

        # runner = web.AppRunner(app)
        # await runner.setup()
        # site = web.TCPSite(runner, host, port)
        printLog('top of myrunapp')
        # self.app.run(host="localhost", port=11311)
        await self.app.run(
            host=self.app.config["HOST_ADDRESS"],
            port=self.app.config["PORT"])
        printLog('awaiting run in myrunapp')

        while True:
            printLog('waiting')
            await asyncio.sleep(3600)  # sleep forever

    async def application(scope, receive, send):
        event = await receive()
        await send({"type": "websocket.send", "content": False})
        # ASGI_APP = WSGIMiddleware(flaskContext.app)


async def http_server_loop(appCtx: flaskContext) -> None:
    try:
        printLog('Trying to launch http server')
        await appCtx.my_run_app()  # .app.run()
        printLog('after launching http server')
    except e:
        printLog(f"error: {e}")
    finally:
        printLog('http_server_loop ended')

if __name__ == '__main__':
    flaskContext.app.run(host="localhost", port=11311)

# class Webserver:
#     def __init__(self, ctx: ProxyGameContext):
#         self.app = web.Application()
#         self.host = "localhost"
#         self.port = "11311"
#         self.ctx = ctx

#         self.connected = False

#     async def initializer(self) -> web.Application:
#         self.app.router.add_post('/Locations', self.ctx.locationHandler)
#         self.app.router.add_post('/Goal', self.ctx.goalHandler)
#         self.app.router.add_post('/Death', self.ctx.deathHandler)
#         self.app.router.add_get('/Deathpoll', self.ctx.deathpollHandler)
#         self.app.router.add_get('/Items', self.ctx.itemsHandler)
#         self.app.router.add_get('/Datapackage', self.ctx.datapackageHandler)
#         return self.app

#     async def my_run_app(self, app, host, port):
#         runner = web.AppRunner(app)
#         await runner.setup()
#         site = web.TCPSite(runner, host, port)
#         await site.start()

#         while True:
#             await asyncio.sleep(3600)  # sleep forever

#     async def run(self):
#         if not self.connected:
#             await self.my_run_app(
#                 app=await self.initializer(),
#                 host=self.host, port=self.port
#                 )
#             self.connected = True
#             return self.connected
#         else:
#             logger.info('Already connected')
#             return


# async def http_server_loop(wb: Webserver) -> None:
#     try:
#         logger.info('Trying to launch http server')
#         await wb.run()
#     finally:
#         logger.info('http_server_loop ended')
#     # TODO: handle exceptions in some way like this
#     # except websockets.InvalidMessage:
#     #     # probably encrypted
#     #     if address.startswith("ws://"):
#     #         # try wss
#     #         await server_loop(ctx, "ws" + address[1:])
#     #     else:
#     #         ctx.handle_connection_loss(f"Lost connection to the multiworld server due to InvalidMessage"
#     #                                    f"{reconnect_hint()}")
#     # except ConnectionRefusedError:
#     #     wb.ctx.handle_connection_loss("Connection refused by the server. "
#     #                                "May not be running Archipelago on that address or port.")
#     # # except websockets.InvalidURI:
#     # #     wb.ctx.handle_connection_loss("Failed to connect to the multiworld server (invalid URI)")
#     # except OSError:
#     #     wb.ctx.handle_connection_loss("Failed to connect to the multiworld server")
#     # except Exception:
#     #     wb.ctx.handle_connection_loss(f"Lost connection to the multiworld server{reconnect_hint()}")
#     # finally:
#     #     await wb.ctx.connection_closed()
#     #     if wb.ctx.server_address and wb.ctx.username and not wb.ctx.disconnected_intentionally:
#     #         logger.info(f"... automatically reconnecting in {wb.ctx.current_reconnect_delay} seconds")
#     #         assert wb.ctx.autoreconnect_task is None
#     #         wb.ctx.autoreconnect_task = asyncio.create_task(server_autoreconnect(wb.ctx), name="server auto reconnect")
#     #     wb.ctx.current_reconnect_delay *= 2


# if __name__ == '__main__':
#     ctx = ProxyGameContext("localhost", "")
#     webserver = Webserver(ctx)
#     webserver.run()
