import asyncio
import json
from websockets.asyncio.server import serve, ServerConnection

#from .MinitClient import ProxyGameContext

ProxyGameContext = object

class proxy_client:
    def __init__(self, ctx):
        self.ctx = ctx
        self.host = "localhost"
        self.port = 11311

    async def run(self):
        server = await serve(self.echo, self.host, self.port)
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
                    message = json.dumps({"type": "deathlink"})
                elif type == "knockback":
                    pass

                if message is not None:
                    await websocket.send(message)
        finally:
            self.ctx.socket_server = None


def socket_server_loop(ctx: ProxyGameContext):
    prox = proxy_client(ctx)
    asyncio.run(prox.run())

if __name__ == "__main__":
    socket_server_loop(None)
