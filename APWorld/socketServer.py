import asyncio
import json
from websockets.asyncio.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedError

#from .MinitClient import ProxyGameContext

ProxyGameContext = object

class proxy_client:
    def __init__(self, ctx):
        self.ctx = ctx
        self.host = "localhost"
        self.port = 11311

    async def run(self):
        server = await serve(self.echo, self.host, self.port, ping_interval=None)  # TODO: see if i can get gamemaker to respect ping/pong and turn this back on
        try:
            await server.serve_forever()
        finally:
            self.ctx.socket_server = None

    async def echo(self, websocket: ServerConnection):
        # run once per connection to the open socket
        assert self.ctx.socket_server is None, "duplicate client/game connection"
        self.ctx.socket_server = websocket
        try:
            async for incoming in websocket:
                data = json.loads(incoming)
                type = data["type"]
                message = None
                if type == "locations":
                    locs = await self.ctx.locationHandler(data["locations"])
                    message = locs  #?
                elif type == "goal":
                    await self.ctx.goalHandler(data["goal"])
                elif type == "death":
                    await self.ctx.deathHandler()
                elif type == "knockback":
                    pass
                elif type == "er_connections":
                    message = await self.ctx.erConnHandler()
                elif type == "items":
                    message = await self.ctx.itemsHandler()

                if message is not None:
                    await websocket.send(message)
        except ConnectionClosedError:
            pass  # TODO: log
        finally:
            self.ctx.socket_server = None


def socket_server_loop(ctx: ProxyGameContext):
    prox = proxy_client(ctx)
    asyncio.run(prox.run())

if __name__ == "__main__":
    socket_server_loop(None)
