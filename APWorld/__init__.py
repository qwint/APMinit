from worlds.AutoWorld import World, WebWorld
from BaseClasses import (
    Region,
    Location,
    Item,
    ItemClassification,
    Entrance,
    Tutorial
)
from .Items import (
    MinitItem,
    MinitItemData,
    item_table,
    item_frequencies,
    item_groups
)
from .Locations import location_table
from .Regions import region_table
from .ERData import (
    er_regions,
    er_entrances,
    minit_get_target_groups,
    er_static_connections,
    door_names,
)
from .Options import MinitGameOptions
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from .Rules import MinitRules
from .ER_Rules import ER_MinitRules
from typing import Dict, Any, List
from worlds.LauncherComponents import (
    Component,
    components,
    Type,
    launch_subprocess
)
import random
from Utils import visualize_regions
from EntranceRando import randomize_entrances  # , ER_Entrance

# high prio
# TODO - find more places exceptions need to be handled
# TODO - confirm each sword does correct effects per sword
# - (pushback, damage, etc.)
# TODO - figure out how to add tests and test for
# - confirm a sword or swim is in the first two checks
# - confirm prog balancing settings (min/loc/items) work
# - confirm the options are working as intended (when added)

# misc game mod TODOs
# TODO - pull all required game mods out and reapply to clean up patch file
# TODO - save mod specific values like location_sent etc.

# add options
# TODO - figure out how to progressive sword
# TODO - add puzzleless to de-prio longer/confusing puzzles
# TODO - add random start locations

# known low prio
# TODO - clean up game mod logging to necessities
# TODO - clean up item/location names
# TODO - refactor code
# TODO - add swim as an option for getting 1/4 of temple coin
# TODO - add coin counter when recieving any new coins

# deathlink testing
# deaths during pause seem to dissapear
# sometimes item pickups are delayed, seems to be competing async tasks in game
# saw a death as i respawned once but no idea what the cause
# still some sort of message queuing in the game mod
# seemingly had another
# - Unable to find any instance for object index '0' name 'Player'
# - at gml_Object_apConnection_Other_62
# error when recieving a deathlink after dying, but unknown why
# - (because that should be handled)
# seemingly unrelated bugs: broken truck seems to not be sending when collected
# potential sync issue when sending items and dying (deathlink)
#  where item_sent is flagged by ap never hears

# bug reports
# hotel residents showing up in their rooms before being saved,
# - potentially because the game was already completed? (toilet)
# shrub arena not getting more enemies/dropping the coin
# sidekick-energy guy not showing up at his dialog spawns
# hotel backroom coin is accessible without breaking the pot
# - (confirm vanilla behavior or fix)
# fanfares sometimes clip you into walls without a way out
# generation breaks sometimes, unknown cause

# ideas to explore
# make teleporter a item/location
# make residents item/location
# make boss fight require the left/right machines
# - to be stopped (and thus swim + coffee + darkroom by default)

# release notes:
# now press Q to return to dog house!
# save files should now correctly represent the % aquired
# ap sync should no longer give you items you already have
# - thus no longer replacing your weapon with a dupe
# - of your most recent recieved item


class MinitWebWorld(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Minit randomizer for AP",
        "English",
        "docs/setup_en.md",
        "setup/en",
        ["qwint"]
    )

    tutorials = [setup]


def launch_client():
    from .MinitClient import launch
    launch_subprocess(launch, name="MinitClient")


components.append(Component(
    "Minit Client",
    "MinitClient",
    func=launch_client,
    component_type=Type.CLIENT,
    ))


class MinitItem(Item):
    game = "Minit"


class MinitWorld(World):
    game = "Minit"
    required_client_version = (0, 4, 3)
    options_dataclass = MinitGameOptions
    options: MinitGameOptions
    web = MinitWebWorld()
    output_connections: List[tuple[str, str]]

    item_name_to_id = {
        name: data.code
        for name, data
        in item_table.items()
        if data.code is not None}
    location_name_to_id = {
        name: data.code
        for name, data
        in location_table.items()
        if data.code is not None}
    locked_locations = {
        name: data
        for name, data
        in location_table.items()
        if data.locked_item}
    item_name_groups = item_groups

    def create_item(self, name: str) -> MinitItem:
        data = item_table[name]
        return MinitItem(name, data.classification, data.code, self.player)

    def create_items(self):
        for item_name, item_data in item_table.items():
            if (item_data.code and item_data.can_create(
                    self.multiworld,
                    self.player)):
                if (item_name in item_frequencies):
                    for count in range(item_frequencies[item_name]):
                        self.multiworld.itempool.append(
                            MinitItem(
                                item_name,
                                item_data.classification,
                                item_data.code,
                                self.player))
                else:
                    self.multiworld.itempool.append(
                        MinitItem(
                            item_name,
                            item_data.classification,
                            item_data.code,
                            self.player))

    def make_bad_map(self) -> List[tuple[str, str]]:
        unconnected = []
        output = []
        for entrance in er_entrances:
            if entrance[0] not in door_names:
                unconnected.append(entrance[0])
        self.random.shuffle(unconnected)
        try:
            while unconnected:
                left = unconnected.pop()
                right = unconnected.pop()
                output.append((left, right))
                output.append((right, left))
        except IndexError:
            print("too many connections, leaving 1 unconnected")
        return output

    def create_regions(self):

        if self.options.er_option == 0:
            # self.output_connections = None
            # self.output_connections = [
            #     ("dog house inside door", "dog house door",),
            #     ("dog house door", "dog house inside door",),

            #     ("dog house west", "dog house east",),
            #     ("dog house east", "dog house west",),

            #     ("dog house east lower", "dog house bushes",),
            #     ("dog house bushes", "dog house east lower",),

            #     ("dog house river north", "dog house river south",),
            #     ("dog house river south", "dog house river north",),

            #     ("dog house south", "coffee shop inside",),
            #     ("coffee shop inside", "dog house south",),
            # ]
            self.output_connections = self.make_bad_map()

            for region_name in region_table.keys():
                self.multiworld.regions.append(Region(
                    region_name,
                    self.player,
                    self.multiworld))

            for loc_name, loc_data in location_table.items():
                if not loc_data.can_create(self.multiworld, self.player):
                    continue
                region = self.multiworld.get_region(
                    loc_data.region,
                    self.player)
                new_loc = Location(
                    self.player,
                    loc_name,
                    loc_data.code,
                    region)
                if (not loc_data.show_in_spoiler):
                    new_loc.show_in_spoiler = False
                region.locations.append(new_loc)
                if loc_name == "Fight the Boss":
                    self.multiworld.get_location(
                        loc_name,
                        self.player
                    ).place_locked_item(MinitItem(
                        name="Boss dead",
                        classification=ItemClassification.progression,
                        code=60021,
                        player=self.player))

            for region_name, exit_list in region_table.items():
                region = self.multiworld.get_region(region_name, self.player)
                region.add_exits(exit_list)
        # elif self.options.er_option == 3:
        #     # current map gen is pure random, so make regions/connections vanilla
        #     self.output_connections = self.make_bad_map()

        #     for region_name in region_table.keys():
        #         self.multiworld.regions.append(Region(
        #             region_name,
        #             self.player,
        #             self.multiworld))

        #     for loc_name, loc_data in location_table.items():
        #         if not loc_data.can_create(self.multiworld, self.player):
        #             continue
        #         region = self.multiworld.get_region(
        #             loc_data.region,
        #             self.player)
        #         new_loc = Location(
        #             self.player,
        #             loc_name,
        #             loc_data.code,
        #             region)
        #         if (not loc_data.show_in_spoiler):
        #             new_loc.show_in_spoiler = False
        #         region.locations.append(new_loc)
        #         if loc_name == "Fight the Boss":
        #             self.multiworld.get_location(
        #                 loc_name,
        #                 self.player
        #             ).place_locked_item(MinitItem(
        #                 name="Boss dead",
        #                 classification=ItemClassification.progression,
        #                 code=60021,
        #                 player=self.player))

        #     for region_name, exit_list in region_table.items():
        #         region = self.multiworld.get_region(region_name, self.player)
        #         region.add_exits(exit_list)
        elif self.options.er_option == 1:
            # current code for using the Generic ER randomizer, but as it isn't
            # finished yet delegating to an impossible option
            region_list = []
            for region_name in er_regions:
                region = Region(
                    region_name,
                    self.player,
                    self.multiworld)
                self.multiworld.regions.append(region)
                region_list.append(region)

            for region_name, exit_list in er_static_connections.items():
                region = self.multiworld.get_region(region_name, self.player)
                for other_region_name in exit_list:
                    other_region = self.multiworld.get_region(other_region_name, self.player)
                    region.connect(other_region)
                # region = self.multiworld.get_region(region_name, self.player)
                # region_list.append(region)
                # region.add_exits(exit_list)
                # for region2 in exit_list:
                #     self.multiworld.get_region(
                #         region2,
                #         self.player
                #     ).add_exits([region_name])
                # for exit in region.exits:
                #     print(f"for static connection: {exit.name} parent region: {exit.parent_region} and connected region: {exit.connected_region}")

            # entrance_list = []
            # exit_list = []
            for er_entrance in er_entrances:
                region = self.multiworld.get_region(
                    er_entrance[1],
                    self.player)
                # entrance = ER_Entrance(self.player, er_entrance[0], region)
                # entrance.is_dead_end = er_entrance[2]
                # entrance.group_name = er_entrance[3]
                # entrance_list.append(entrance)
                # print(f"for exit: {entrance.name} parent region: {entrance.parent_region} and connected region: {entrance.connected_region}")
                # region = self.multiworld.get_region(region_name, self.player)
                en1 = region.create_exit(er_entrance[0])
                en2 = region.create_er_entrance(er_entrance[0])
                # en1.er_group = er_entrance[3]
                # en2.er_group = er_entrance[3]

                # print(f"current entrance {entrance_list[len(entrance_list) - 1].name} is type: {type(entrance_list[len(entrance_list) - 1])}")
                # for exit in region.get_exits():
                #     print(f"for ER connection: {exit.name} parent region: {exit.parent_region} and connected region: {exit.connected_region}")
                #     print(f"region {region.name} has exits: {type(exit)}")
                # for exit in region.get_exits():
                #     print(f"region {region.name} has exits: {type(exit)}")

            # test = ""
            # needed_region = self.multiworld.get_region(
            #     'plant bushes',
            #     self.player)
            # for entrance in self.multiworld.get_region(
            #         'dog house west',
            #         self.player).exits:
            #     is_dog_house = entrance.name == 'dog house door'
            #     if not entrance.connected_region and not is_dog_house:
            #         self.multiworld.register_indirect_condition(
            #             needed_region,
            #             entrance)
            #         entrance.access_rule = lambda state: state.can_reach(
            #             needed_region,
            #             "Region",
            #             self.player)
                # else:
                #     test += entrance.name
            # assert test == "garbage", f"test was {test}"
            # print("region_list: " + str(region_list))

            self.output_connections = randomize_entrances(
                self,
                # self.player,
                self.random,
                # entrance_list,
                region_list,
                True,
                minit_get_target_groups,
                # True,
                )
            # print("output_connections: " + str(output_connections))
            # output_coordinates = transform_connections(output_connections)
            # assert self.output_connections == "garbage", f"test was {self.output_connections}"

            for loc_name, loc_data in location_table.items():
                if not loc_data.can_create(self.multiworld, self.player):
                    continue
                region = self.multiworld.get_region(
                    loc_data.er_region,
                    self.player)
                new_loc = Location(
                    self.player,
                    loc_name,
                    loc_data.code,
                    region)
                if (not loc_data.show_in_spoiler):
                    new_loc.show_in_spoiler = False
                region.locations.append(new_loc)
                if loc_name == "Fight the Boss":
                    self.multiworld.get_location(
                        loc_name,
                        self.player
                    ).place_locked_item(MinitItem(
                        name="Boss dead",
                        classification=ItemClassification.progression,
                        code=60021,
                        player=self.player))
            visualize_regions(
                self.multiworld.get_region("Menu", self.player),
                "output/regionmap.puml")
            # print(output_connections)
            # randomize_entrances(self, self, self, self, self, self, self)

        # Locked location logic from Pseudoregalia, will likely need for sword
        # Place locked locations.
        # for location_name, location_data in self.locked_locations.items():
        #     if not location_data.can_create(self.multiworld, self.player):
        #         continue

        #     # # Doing this really stupidly because breaker's locking will change after logic rework is done
        #     # if location_name == "Dilapidated Dungeon - Dream Breaker":
        #     #     if bool(self.multiworld.progressive_breaker[self.player]):
        #     #         locked_item = self.create_item("Progressive Dream Breaker")
        #     #         self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)
        #     #         continue

        #     locked_item = self.create_item(location_table[location_name].locked_item)
        #     self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "slot_number": self.player,
            "death_link": self.options.death_link.value,
            "death_amnisty_total": self.options.death_amnisty_total.value,
            "ER_connections": self.output_connections,
            }

    def set_rules(self):
        if self.options.er_option == 0:
            minitRules = MinitRules(self)
            minitRules.set_Minit_rules()
        # elif self.options.er_option == 3:
        #     minitRules = MinitRules(self)
        #     minitRules.set_Minit_rules()
        elif self.options.er_option == 1:
            minitRules = ER_MinitRules(self)
            minitRules.set_Minit_rules()

        if self.options.chosen_goal == 0:  # boss fight
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.has("Boss dead", self.player)
        elif self.options.chosen_goal == 1:  # toilet
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.has("ItemBrokenSword", self.player) and \
                (minitRules.region_factory_desert(state) or
                    minitRules.region_factory_hotel(state))
        elif self.options.chosen_goal == 2:  # any
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.has("Boss dead", self.player) or \
                (state.has("ItemBrokenSword", self.player) and
                    (minitRules.region_factory_desert(state) or
                        minitRules.region_factory_hotel(state)))
        if bool(self.options.starting_sword.value):
            self.multiworld.local_early_items[self.player]['ItemSword'] = 1

    def get_filler_item_name(self) -> str:
        return "HeartPiece"
