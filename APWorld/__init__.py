from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Item, ItemClassification, Entrance, Tutorial
from .Items import MinitItem, MinitItemData, item_table, item_frequencies, item_groups
from .Locations import location_table
from .Regions import region_table
from .Options import MinitGameOptions
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from .Rules import MinitRules
from typing import Dict, Any
from worlds.LauncherComponents import Component, components, Type, launch_subprocess

#high prio
#TODO - find more places exceptions need to be handled
#TODO - confirm each sword does correct effects per sword (pushback, damage, etc.)
#TODO - figure out how to add tests and test for
            #confirm a sword or swim is in the first two checks
            #confirm prog balancing settings (min/loc/items) work
            #confirm the options are working as intended (when added)
#TODO - extra coins/tentacle/hearts given on local items
#TODO - fanfares don't pause timer, and you can take damage ticks during them

#misc game mod TODOs
#TODO - pull all required game mods out and reapply to clean up patch file
#TODO - save mod specific values like location_sent etc.

#add options
#TODO - figure out how to progressive sword
#TODO - add puzzleless to de-prio longer/confusing puzzles
#TODO - add random start locations

#known low prio
#TODO - clean up game mod logging to necessities
#TODO - clean up item/location names
#TODO - refactor code
#TODO - add swim as an option for getting 1/4 of temple coin

#bug reports
#hotel residents showing up in their rooms before being saved, potentially because the game was already completed? (toilet)
#shrub arena not getting more enemies/dropping the coin
#sidekick-energy guy not showing up at his dialog spawns
#hotel backroom coin is accessible without breaking the pot (confirm vanilla behavior or fix)
#fanfares sometimes clip you into walls without a way out
#generation breaks sometimes, unknown cause

#ideas to explore
#make teleporter a item/location
#make residents item/location
#make boss fight require the left/right machines to be stopped (and thus swim + coffee + darkroom by default)

#release notes: 
#now press Q to return to dog house!
#save files should now correctly represent the % aquired
#ap sync should no longer give you items you already have thus no longer replacing your weapon with a dupe of your most recent recieved item

class MinitWebWorld(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Minit randomizer connected to an Archipelago Multiworld",
        "English",
        "docs/setup_en.md",
        "setup/en",
        ["qwint"]
    )


    tutorials = [setup]


def launch_client():
    from .MinitClient import launch
    launch_subprocess(launch, name="MinitClient")


components.append(Component("Minit Client", "MinitClient", func=launch_client, component_type=Type.CLIENT))

class MinitItem(Item):
    game = "Minit"

class MinitWorld(World):
    game = "Minit"
    required_client_version = (0, 4, 3)
    options_dataclass = MinitGameOptions
    options: MinitGameOptions
    web = MinitWebWorld()


    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}
    locked_locations = {name: data for name, data in location_table.items() if data.locked_item}
    item_name_groups = item_groups

    def create_item(self, name: str) -> MinitItem:
        data = item_table[name]
        return MinitItem(name, data.classification, data.code, self.player)

    def create_items(self):
        for item_name, item_data in item_table.items():
            if (item_data.code and item_data.can_create(self.multiworld, self.player)):
                if (item_name in item_frequencies):
                    for count in range(item_frequencies[item_name]):
                        self.multiworld.itempool.append(MinitItem(item_name,
                                                             item_data.classification,
                                                             item_data.code,
                                                             self.player))
                else:
                    self.multiworld.itempool.append(MinitItem(item_name,
                                                         item_data.classification,
                                                         item_data.code,
                                                         self.player))

    def create_regions(self):
        for region_name in region_table.keys():
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        for loc_name, loc_data in location_table.items():
            if not loc_data.can_create(self.multiworld, self.player):
                continue
            region = self.multiworld.get_region(loc_data.region, self.player)
            new_loc = Location(self.player, loc_name, loc_data.code, region)
            if (not loc_data.show_in_spoiler):
                new_loc.show_in_spoiler = False
            region.locations.append(new_loc)
            if loc_name == "Fight the Boss":
                self.multiworld.get_location(loc_name, self.player).place_locked_item(MinitItem(name = "Boss dead", classification = ItemClassification.progression, code = 60021, player = self.player))

        for region_name, exit_list in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exit_list)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"slot_number": self.player,}

    def set_rules(self):
        minitRules = MinitRules(self)
        minitRules.set_Minit_rules()
        if self.options.chosen_goal == 0: #boss fight
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player)
        elif self.options.chosen_goal == 1: #toilet
            self.multiworld.completion_condition[self.player] = lambda state: state.has("ItemBrokenSword", self.player) and (minitRules.region_factory_desert(state) or minitRules.region_factory_hotel(state))
        elif self.options.chosen_goal == 2: #any
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player) or (state.has("ItemBrokenSword", self.player) and (minitRules.region_factory_desert(state) or minitRules.region_factory_hotel(state)))
        if (bool(self.options.starting_sword.value) == True):
            self.multiworld.local_early_items[self.player]['ItemSword'] = 1

    def get_filler_item_name(self) -> str:
        return "HeartPiece"