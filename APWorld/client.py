import asyncio
import json
import time
import typing

import Utils
from CommonClient import (
    get_base_parser,
    handle_url_arg,
    logger,
    server_loop,
)
from NetUtils import ClientStatus, RawJSONtoTextParser

from .er_data import er_entrances, game_entrances

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerCommandProcessor as SuperCommandProcessor
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import ClientCommandProcessor as SuperCommandProcessor
    from CommonClient import CommonContext as SuperContext


DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111


class MinitCommandProcessor(SuperCommandProcessor):
    def _cmd_patch(self):
        """Deprecated, use Mod Manager."""
        logger.info("Use Mod Manager")

    def _cmd_amnisty(self, total: int = 1):
        """Set the Death Amnisty value. Default 1."""
        self.ctx.death_amnisty_total = int(total)
        self.ctx.death_amnisty_count = 0
        logger.info(f"Amnisty set to {self.ctx.death_amnisty_total}. \
            Deaths towards Amnisty reset.")


class ProxyGameContext(SuperContext):
    game = GAMENAME

    proxy_task: asyncio.Task[None] | None = None
    socket_server = None  # TODO: type this with ServerConnection

    command_processor = MinitCommandProcessor
    tags: typing.ClassVar = {"KnockbackLink"}
    last_sent_death: float = time.time()
    slot_data: dict[str, any]
    death_amnisty_total: int
    death_amnisty_count: int
    goals: list[str]

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gamejsontotext = RawJSONtoTextParser(self)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []
        self.death_amnisty_total = 1  # should be rewritten by slot data
        self.death_amnisty_count = 0

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Minit Client"
        return ui

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.death_amnisty_total = self.slot_data["death_amnisty_total"]
            # if load(self.locations_info):
            #     load(self.locations_info)
            # else:
            Utils.async_start(self.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.missing_locations),
                "create_as_hint": 0
                }]))
            self.goals = self.slot_data["goals"]
            Utils.async_start(self.update_death_link(self.slot_data["death_link"]))

        # if cmd == 'LocationInfo':
        #     save(self.locations_info)
        if cmd == "ReceivedItems":
            self.send_to_socket(self.build_item_response())
        if cmd == "Bounced" and "data" in args:
            source_name = args["data"].get("source")
            if source_name is None:
                pass
            elif "KnockbackLink" in args["tags"] and source_name != self.player_names[self.slot]:
                if "KnockbackLink" in self.tags:
                    self.send_to_socket({
                        "type": "knockback",
                        "x": args["data"]["value"]["x"],
                        "y": args["data"]["value"]["z"],
                    })
                    # switches y/z to convert between knockback link and gamemaker

    def send_to_socket(self, data: json):
        if self.socket_server is not None:
            Utils.async_start(self.socket_server.send(json.dumps(data)))

    async def send_death(self, death_text: str = ""):
        self.death_amnisty_count += 1
        if self.death_amnisty_count == self.death_amnisty_total:
            await super().send_death(death_text)
            self.last_sent_death = time.time()
            self.death_amnisty_count = 0

    async def knockback_handler(self, x: int, y: int) -> None:
        """handle KnockbackLink packets from client"""
        if "KnockbackLink" not in self.tags:
            return
        Utils.async_start(self.send_msgs([{
            "cmd": "Bounce",
            "tags": ["KnockbackLink"],
            "data": {
                "source": self.player_names[self.slot],
                "cause": f"{self.player_names[self.slot]} got hit",
                "time": time.time(),
                "value": {
                    "x": x,
                    "y": 0,
                    "z": y,  # switch y/z to convert between knockback link and gamemaker
                }
            }
        }]))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    async def location_handler(self, locations: list[int]) -> str:
        """handle locations data from game and use scouts to return useful info"""
        await self.check_locations(locations)

        local_response = self.build_local_locations_response(locations)
        return json.dumps(local_response)

    async def goal_handler(self, goal: str) -> None:
        """handle goal attempt from game checking for enabled goals before sending to server"""
        response = self.build_goal_response(goal)
        if response:
            await self.send_msgs(response)

    async def death_handler(self) -> None:
        """handle death ping from game"""
        if self.slot_data["death_link"]:
            await self.send_death(f"{self.player_names[self.slot]} ran out of time")  # consider more silly messages

    async def items_handler(self) -> str:
        """handle item sync from game"""
        return json.dumps(self.build_item_response())

    async def er_conn_handler(self) -> str:
        """handle er connection sync from game"""
        response = self.build_er_response()
        return json.dumps(response)

    def on_deathlink(self, data: dict[str, typing.Any]) -> None:
        # CommonClient function run on received deathlinks
        super().on_deathlink(data)
        self.send_to_socket({"type": "death"})

    def build_er_response(self):
        """
        er_message format:
        {"type": "entrance_connections",
         "enabled": True,
         "Entrances": [
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
        er_message = {"type": "entrance_connections", "enabled": True}
        connections = self.slot_data["ER_connections"]
        if not connections:
            er_message["enabled"] = False
            return er_message
        er_data_lookup = {data.entrance_name: data for data in er_entrances}
        er_message["Entrances"] = game_entrances
        for connection in connections:
            left, right = connection
            left_entrance = er_data_lookup[left]
            right_entrance = er_data_lookup[right]
            left_tile = left_entrance.room_tile
            left_name = left_entrance.entrance_name

            for index, entrance in enumerate(er_message["Entrances"][left_tile]):
                if left_name == entrance["CName"]:
                    er_message["Entrances"][left_tile][index]["out"] = {
                        "tile": right_entrance.room_tile,
                        "x": right_entrance.x_cord,
                        "y": right_entrance.y_cord,
                        "offDir": right_entrance.offset_direction,
                        "offNum": right_entrance.offset_value,
                        }

        return er_message

    def build_goal_response(self, request: str):
        if request in self.goals:
            goalmessage = [{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
                }]
        else:
            goalmessage = None
        return goalmessage

    def build_local_locations_response(self, locations: list[int]) -> json:
        """
        expecting request to be json body in the form of
        {"type": "location_response", "Player": "qwint", "Item": "ItemGrinder", "Code": 60017}
        - for a local item
        {"type": "location_response", "Player": "OtherPlayer", "Item": "ItemGrinder"}
        - for a remote item
        """

        locations = set(locations).difference(self.locations_checked)
        if len(locations) != 1:
            return {"type": "location_response", "Location": "Not found in scout cache"}
            # TODO update if client can handle

        location = locations.pop()
        if not self.locations_info:
            return {"type": "location_response", "Location": "Not found in scout cache"}
            # TODO update if client can handle

        if location not in self.locations_info:
            return {"type": "location_response", "Location": "Not found in scout cache"}
            # TODO update if client can handle

        loc = self.locations_info[location]
        slot = loc.player
        player = self.slot_info[loc.player].name
        item = self.item_names.lookup_in_slot(loc.item, slot)
        code = loc.item

        if self.slot_concerns_self(slot):
            locationmessage = {
                "type": "location_response",
                "Player": player,
                "Item": item,
                "Code": code}
        else:
            locationmessage = {"type": "location_response", "Player": player, "Item": item}
        return locationmessage

    def build_item_response(self):
        """
        expecting request to be json body in the form of
        {"type": "items", "Items": [123,456],"Coins":2, "Hearts": 1, "Tentacles":4}
        """
        item_ids = []
        coins = 0
        hearts = 0
        tentacles = 0
        swords_f = 0
        swords_r = 0
        for item in self.items_received:
            # TODO - change to lookup ids for actual item names
            if item[0] == 60000:
                coins += 1
            elif item[0] == 60001:
                hearts += 1
            elif item[0] == 60002:
                tentacles += 1
            elif item[0] == 60021:
                swords_f += 1
            elif item[0] == 60022:
                swords_r += 1
            else:
                item_ids.append(item[0])
        return {
            "type": "items",
            "Items": item_ids,
            "Coins": coins,
            "Hearts": hearts,
            "Tentacles": tentacles,
            "swordsF": swords_f,
            "swordsR": swords_r,
        }


async def main(args):
    from .socket_server import ProxyClient

    ctx = ProxyGameContext(args.connect, args.password)
    prox = ProxyClient(ctx)
    ctx.proxy_task = asyncio.create_task(prox.run(), name="websocket loop")
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if tracker_loaded:
        ctx.run_generator()
    if Utils.gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch(*args):
    import colorama

    parser = get_base_parser(description="Minit Archipelago Client.")
    parser.add_argument("url", nargs="?", help="Archipelago Webhost uri to auto connect to.")
    args = parser.parse_args(args)

    args = handle_url_arg(args, parser=parser)

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == "__main__":
    import sys
    launch(*sys.argv[-1:])
