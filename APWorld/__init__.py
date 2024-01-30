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


try:
    from EntranceRando import randomize_entrances
    er_loaded = True
except ModuleNotFoundError:
    er_loaded = False
#TODO - save mod specific values like location_sent etc.


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

# add options
# TODO - figure out how to progressive sword
# TODO - add puzzleless to de-prio longer/confusing puzzles
# TODO - add random start locations

# known low prio
# TODO - clean up game mod logging to necessities
# TODO - clean up item/location names
# TODO - refactor code
# TODO - add swim as an option for getting 1/4 of temple coin

# deathlink testing
# deaths during pause seem to dissapear
# saw a death as i respawned once but no idea what the cause
# seemingly had another
# - Unable to find any instance for object index '0' name 'Player'
# - at gml_Object_apConnection_Other_62
# error when recieving a deathlink after dying, but unknown why
# - (because that should be handled)
# potential sync issue when sending items and dying (deathlink)
#  where item_sent is flagged by ap never hears

# bug reports
# hotel backroom coin is accessible without breaking the pot
# fanfares sometimes clip you into walls without a way out
# generation breaks sometimes, unknown cause

# ideas to explore
# make teleporter a item/location
# make residents item/location
# make boss fight require the left/right machines
# - to be stopped (and thus swim + coffee + darkroom by default)
# set item_sent flags on connect / full sync


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
    """
    Minit is a peculiar little adventure played sixty seconds at a time.
    """

    game = "Minit"
    required_client_version = (0, 4, 3)
    options_dataclass = MinitGameOptions
    options: MinitGameOptions
    web = MinitWebWorld()
    output_connections: List[tuple[str, str]]
    er_region_list: List[Region] = []

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

    def add_regions_and_locations(self, er_on: bool):
        if er_on:
            region_list = er_regions
            entrance_list = er_static_connections
        else:
            region_list = region_table.keys()
            entrance_list = region_table
        for region_name in region_list:
            self.multiworld.regions.append(Region(
                region_name,
                self.player,
                self.multiworld))

        for loc_name, loc_data in location_table.items():
            if not loc_data.can_create(self.multiworld, self.player):
                continue
            if er_on:
                loc_region = loc_data.er_region
            else:
                loc_region = loc_data.region
            region = self.multiworld.get_region(
                loc_region,
                self.player)
            new_loc = Location(
                self.player,
                loc_name,
                loc_data.code,
                region)
            if (not loc_data.show_in_spoiler):
                new_loc.show_in_spoiler = False
            region.locations.append(new_loc)
            if loc_data.locked_item:
                self.multiworld.get_location(
                    loc_name,
                    self.player
                ).place_locked_item(MinitItem(
                    name=loc_data.locked_item,
                    classification=ItemClassification.progression,
                    code=None,
                    player=self.player))

        for region_name, exit_list in entrance_list.items():
            region = self.multiworld.get_region(region_name, self.player)
            if er_on:
                for other_region_name in exit_list:
                    other_region = self.multiworld.get_region(
                        other_region_name,
                        self.player,
                        )
                    region.connect(other_region)
                    other_region.connect(region)
            else:
                region.add_exits(exit_list)
        # elif self.options.er_option == 1:
        #     # current map gen is pure random, so make regions/connections vanilla
        #     self.output_connections = self.make_bad_map()

    def create_regions(self):

        er_on = bool(self.options.er_option)

        if er_on and er_loaded:
            self.add_regions_and_locations(er_on)  # will move this back up when er is finished
            # current code for using the Generic ER randomizer
            if self.multiworld.players == 1:
                # if there is a one-player world, make at least one
                # of the early entrances into a check
                # that you can pick up for free
                free_checks = [
                    "watering can",  # deadend
                    "camera house outside south",  # deadend
                    "glove outside east",
                    "glove outside west",
                    "factory loading upper north",
                    "factory loading upper east",
                    "factory loading upper south",
                    "factory snakehall north",
                    "factory queue",  # deadend
                    "trophy room",  # deadend
                    ]  # consider removing the deadends because they could have a higher chance of killing the seed
                self.random.shuffle(free_checks)
                starting_entrance = free_checks.pop()
                # print(f"adding {starting_entrance} to starting region to make single player ER playable")
                manual_connect_start = None
                manual_connect_end = None
                # add_manual_connect = True

            for er_entrance in er_entrances:
                region = self.multiworld.get_region(
                    er_entrance[1],
                    self.player)
                if region not in self.er_region_list:
                    self.er_region_list.append(region)
                # entrance.is_dead_end = er_entrance[2]

                en1 = region.create_exit(er_entrance[0])
                en1.er_type = Entrance.EntranceType.TWO_WAY
                en1.er_group = er_entrance[3]
                if starting_entrance and er_entrance[0] in ["dog house south", starting_entrance]:
                    if er_entrance[0] == "dog house south":
                        manual_connect_start = en1
                    if er_entrance[0] == starting_entrance:
                        manual_connect_end = en1
                    if manual_connect_start and manual_connect_end:
                        manual_connect_start.connect(manual_connect_end.parent_region)
                        manual_connect_end.connect(manual_connect_start.parent_region)
                        # print(f"connecting {manual_connect_start.name} and {manual_connect_end.name}")
                        # add_manual_connect = False
                else:
                    en2 = region.create_er_target(er_entrance[0])
                    en2.er_type = Entrance.EntranceType.TWO_WAY
                    en2.er_group = er_entrance[3]

        elif er_on and not er_loaded:
            self.add_regions_and_locations(False)
            self.output_connections = self.make_bad_map()
        else:
            self.add_regions_and_locations(er_on)  # will move this back up when er is finished
            self.output_connections = None
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
            # self.output_connections = self.make_bad_map()

    def parse_goals(self, chosen_goal: int) -> List[str]:
        if chosen_goal == 0:  # boss fight
            return ["boss"]
        if chosen_goal == 1:  # toilet
            return ["toilet"]
        if chosen_goal == 2:
            return ["toilet", "boss"]  # any

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "slot_number": self.player,
            "death_link": self.options.death_link.value,
            "death_amnisty_total": self.options.death_amnisty_total.value,
            "ER_connections": self.output_connections,
            "goals": self.parse_goals(self.options.chosen_goal),
            }

    def interpret_slot_data(self, slot_data: Dict[str, Any]):
        if slot_data["ER_connections"]:
            e_dict = {entrance.name: entrance for region in self.multiworld.get_regions(self.player) for entrance in region.entrances}

            for connection in slot_data["ER_connections"]:
                assert connection[0] in e_dict, f"entrance {connection[0]} in slot data not in world"
                assert connection[1] in e_dict, f"entrance {connection[1]} in slot data not in world"

                e_dict[connection[0]].connected_region = e_dict[connection[1]].parent_region

    def set_rules(self):
        if self.options.er_option == 0:
            minitRules = MinitRules(self)
            minitRules.set_Minit_rules()
        elif self.options.er_option == 1 and not er_loaded:
            minitRules = MinitRules(self)
            minitRules.set_Minit_rules()
        elif self.options.er_option == 1 and er_loaded:
            minitRules = ER_MinitRules(self)
            minitRules.set_Minit_rules()

            # shouldn't be needed later:
            assert ["lighthouse lookout", "coffee shop pot stairs", "sewer island", "shoe shop inside", "camera house inside", "dog house inside", "lighthouse inside", "island house", "shoe shop downstairs", "dog house basement"] not in self.er_region_list
            self.output_connections = randomize_entrances(
                    world=self,
                    regions=self.er_region_list,
                    coupled=True,
                    get_target_groups=minit_get_target_groups,
                    preserve_group_order=False
                    ).pairings
            visualize_regions(
                self.multiworld.get_region("Menu", self.player),
                "output/regionmap.puml")

        if self.options.chosen_goal == 0:  # boss fight
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.has("Boss dead", self.player)
        elif self.options.chosen_goal == 1:  # toilet
            self.multiworld.completion_condition[self.player] = lambda state: \
                minitRules.has_brokensword(state) and \
                state.has("Sword Flushed", self.player)
        elif self.options.chosen_goal == 2:  # any
            self.multiworld.completion_condition[self.player] = lambda state: \
                state.has("Boss dead", self.player) or \
                (minitRules.has_brokensword(state) and
                    state.has("Sword Flushed", self.player))
        if bool(self.options.starting_sword.value):
            self.multiworld.local_early_items[self.player][self.get_sword_item_name()] = 1

    def get_sword_item_name(self) -> str:
        if self.options.progressive_sword.value == 0:
            return "Progressive Sword"
        elif self.options.progressive_sword.value == 1:
            return "Reverse Progressive Sword"
        elif self.options.progressive_sword.value == 2:
            return "ItemSword"

    def get_filler_item_name(self) -> str:
        return "HeartPiece"

    def pre_fill(self) -> None:
        if self.multiworld.players == 1 and not bool(self.options.starting_sword.value):
            starting_items = ["ItemSwim", "ItemWateringCan"]
            if self.options.progressive_sword.value == 2:
                starting_items.append("ItemBrokenSword")
                starting_items.append("ItemSword")
                starting_items.append("ItemMegaSword")
            if self.options.progressive_sword.value == 1:
                starting_items.append("Reverse Progressive Sword")
            if self.options.progressive_sword.value == 0:
                starting_items.append("Progressive Sword")
            self.random.shuffle(starting_items)
            self.multiworld.local_early_items[self.player][starting_items.pop()] = 1
