import asyncio
import Utils
import websockets
import functools
from copy import deepcopy
from typing import List, Any, Iterable
from NetUtils import decode, encode, JSONtoTextParser, JSONMessagePart, NetworkItem
from MultiServer import Endpoint
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, get_base_parser

import os

DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111


class ProxyGameJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text


class ProxyGameCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_ProxyGame(self):
        """Check ProxyGame Connection State"""
        if isinstance(self.ctx, ProxyGameContext):
            logger.info(f"ProxyGame Status: {self.ctx.get_ProxyGame_status()}")


class ProxyGameContext(CommonContext):
    command_processor = ProxyGameCommandProcessor
    game = GAMENAME

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.proxy = None
        self.proxy_task = None
        self.gamejsontotext = ProxyGameJSONToTextParser(self)
        self.autoreconnect_task = None
        self.endpoint = None
        self.items_handling = ITEMS_HANDLING
        self.room_info = None
        self.connected_msg = None
        self.game_connected = False
        self.awaiting_info = False
        self.full_inventory: List[Any] = []
        self.server_msgs: List[Any] = []

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ProxyGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def get_ProxyGame_status(self) -> str:
        if not self.is_proxy_connected():
            return "Not connected to " + str(GAMENAME)

        return "Connected to " + str(GAMENAME)
    async def send_msgs_proxy(self, msgs: Iterable[dict]) -> bool:
        """ `msgs` JSON serializable """
        if not self.endpoint or not self.endpoint.socket.open or self.endpoint.socket.closed:
            return False

        if DEBUG:
            logger.info(f"Outgoing message: {msgs}")

        await self.endpoint.socket.send(msgs)
        return True

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def disconnect_proxy(self):
        if self.endpoint and not self.endpoint.socket.closed:
            await self.endpoint.socket.close()
        if self.proxy_task is not None:
            await self.proxy_task

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    def is_proxy_connected(self) -> bool:
        return self.endpoint and self.endpoint.socket.open

    def on_print_json(self, args: dict):
        text = self.gamejsontotext(deepcopy(args["data"]))
        msg = {"cmd": "PrintJSON", "data": [{"text": text}], "type": "Chat"}
        self.server_msgs.append(encode([msg]))

        if self.ui:
            self.ui.print_json(args["data"])
        else:
            text = self.jsontotextparser(args["data"])
            logger.info(text)

    def update_items(self):
        # just to be safe - we might still have an inventory from a different room
        if not self.is_connected():
            return

        self.server_msgs.append(encode([{"cmd": "ReceivedItems", "index": 0, "items": self.full_inventory}]))

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.connected_msg = encode([args])
            if self.awaiting_info:
                self.server_msgs.append(self.room_info)
                self.update_items()
                self.awaiting_info = False

        elif cmd == "ReceivedItems":
            if args["index"] == 0:
                self.full_inventory.clear()

            for item in args["items"]:
                self.full_inventory.append(NetworkItem(*item))

            self.server_msgs.append(encode([args]))

        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]
            self.room_info = encode([args])

        else:
            if cmd != "PrintJSON":
                self.server_msgs.append(encode([args]))

    def run_gui(self):
        from kvui import GameManager

        class ProxyGameManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago " + str(GAMENAME) + " Client"

        self.ui = ProxyGameManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def proxy(websocket, path: str = "/", ctx: ProxyGameContext = None):
    ctx.endpoint = Endpoint(websocket)
    try:
        await on_client_connected(ctx)

        if ctx.is_proxy_connected():
            async for data in websocket:
                if DEBUG:
                    logger.info(f"Incoming message: {data}")

                for msg in decode(data):
                    if msg["cmd"] == "Connect":
                        # Proxy is connecting, make sure it is valid
                        if msg["game"] != str(GAMENAME):
                            logger.info("Aborting proxy connection: game is not " + str(GAMENAME))
                            await ctx.disconnect_proxy()
                            break

                        if ctx.seed_name:
                            seed_name = msg.get("seed_name", "")
                            if seed_name != "" and seed_name != ctx.seed_name:
                                logger.info("Aborting proxy connection: seed mismatch from save file")
                                logger.info(f"Expected: {ctx.seed_name}, got: {seed_name}")
                                text = encode([{"cmd": "PrintJSON",
                                                "data": [{"text": "Connection aborted - save file to seed mismatch"}]}])
                                await ctx.send_msgs_proxy(text)
                                await ctx.disconnect_proxy()
                                break

                        if ctx.connected_msg and ctx.is_connected():
                            await ctx.send_msgs_proxy(ctx.connected_msg)
                            ctx.update_items()
                        continue

                    if not ctx.is_proxy_connected():
                        break

                    await ctx.send_msgs([msg])

    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logger.exception(e)
    finally:
        await ctx.disconnect_proxy()


async def on_client_connected(ctx: ProxyGameContext):
    if ctx.room_info and ctx.is_connected():
        await ctx.send_msgs_proxy(ctx.room_info)
    else:
        ctx.awaiting_info = True


async def main():
    parser = get_base_parser()
    args = parser.parse_args()

    ctx = ProxyGameContext(args.connect, args.password)
    logger.info("Starting " + str(GAMENAME) + " proxy server")
    ctx.proxy = websockets.serve(functools.partial(proxy, ctx=ctx),
                                 host="localhost", port=11311, ping_timeout=999999, ping_interval=999999)
    ctx.proxy_task = asyncio.create_task(proxy_loop(ctx), name="ProxyLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.proxy
    await ctx.proxy_task
    await ctx.exit_event.wait()


async def proxy_loop(ctx: ProxyGameContext):
    try:
        while not ctx.exit_event.is_set():
            if len(ctx.server_msgs) > 0:
                for msg in ctx.server_msgs:
                    await ctx.send_msgs_proxy(msg)

                ctx.server_msgs.clear()
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.exception(e)
        logger.info("Aborting ProxyGame Proxy Client due to errors")


if __name__ == '__main__':
    Utils.init_logging("ProxyGameClient")
    options = Utils.get_options()

    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()

def launch():
    import colorama
    global executable, server_settings, server_args
    colorama.init()

    # if server_settings:
    #     server_settings = os.path.abspath(server_settings)
    # if not isinstance(options["factorio_options"]["filter_item_sends"], bool):
    #     logging.warning(f"Warning: Option filter_item_sends should be a bool.")
    # initial_filter_item_sends = bool(options["factorio_options"]["filter_item_sends"])
    # if not isinstance(options["factorio_options"]["bridge_chat_out"], bool):
    #     logging.warning(f"Warning: Option bridge_chat_out should be a bool.")
    # initial_bridge_chat_out = bool(options["factorio_options"]["bridge_chat_out"])

    # if not os.path.exists(os.path.dirname(executable)):
    #     raise FileNotFoundError(f"Path {os.path.dirname(executable)} does not exist or could not be accessed.")
    # if os.path.isdir(executable):  # user entered a path to a directory, let's find the executable therein
    #     executable = os.path.join(executable, "factorio")
    # if not os.path.isfile(executable):
    #     if os.path.isfile(executable + ".exe"):
    #         executable = executable + ".exe"
    #     else:
    #         raise FileNotFoundError(f"Path {executable} is not an executable file.")

    if server_settings and os.path.isfile(server_settings):
        server_args = (
            "--rcon-port", rcon_port,
            "--rcon-password", rcon_password,
            "--server-settings", server_settings,
            *rest)
    else:
        server_args = ("--rcon-port", rcon_port, "--rcon-password", rcon_password, *rest)

    asyncio.run(main(args, initial_filter_item_sends, initial_bridge_chat_out))
    colorama.deinit()