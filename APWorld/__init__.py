from worlds.AutoWorld import World
from BaseClasses import Region, Location, Item, ItemClassification, Entrance
from .generic_er import randomize_entrances, ER_Entrance
from .Items import MinitItem, MinitItemData, item_table, item_frequencies, item_groups
from .Locations import location_table
from .Regions import region_table
from .ERData import er_regions, er_entrances, minit_get_target_groups, er_static_connections
from .Options import MinitGameOptions
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from .Rules import MinitRules
from .ER_Rules import ER_MinitRules
from typing import Dict, Any
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
import random
from Utils import visualize_regions

#high prio
#TODO - find more places exceptions need to be handled
#TODO - confirm upgraded swords do the upgraded damage
#TODO - find and squash the local heart crashing on fanfare destroy issue
#TODO - figure out how to add tests and test for
            #confirm a sword or swim is in the first two checks
            #confirm prog balancing settings (min/loc/items) work
            #confirm the options are working as intended (when added)

#misc game mod TODOs
#TODO - pull all required game mods out and reapply to clean up patch file

#add options
#TODO - figure out how to progressive sword
#TODO - add puzzleless to de-prio longer/confusing puzzles
#TODO - add random start locations

#known low prio
#TODO - research why save file percents are inflating - the items += trigger is the count of 
#TODO - add a warp back to doghouse (not really needed, but may be required for island shack logic and/or underground tent logic) (workaround: make a new save, what does that break?)
#TODO - see if more factory checks can be handled with drillshortcut
#TODO - figure out how to protect launching a non-ap save (don't think it matters because the app is different? but maybe if you use same folder??)
#TODO - clean up game mod logging to necessities
#TODO - clean up item/location names
#TODO - refactor code
#TODO - update Temple Coin logic to take into account non-teleport swimming routes (and thus non-teleport routes for other houses)

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
#look into adding another free/wateringCan check in sphere1 to add the vanilla heart back in and expand locations



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

        if self.options.er_option == 0:
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
        elif self.options.er_option == 1:
            for region_name in er_regions:
                 self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

            for region_name, exit_list in er_static_connections.items():
                region = self.multiworld.get_region(region_name, self.player)
                region.add_exits(exit_list)
                # for exit in region.exits:
                #     print(f"for static connection: {exit.name} parent region: {exit.parent_region} and connected region: {exit.connected_region}")


            entrance_list = []
            exit_list = []
            for er_entrance in er_entrances:
                region = self.multiworld.get_region(er_entrance[1], self.player)
                entrance = ER_Entrance(self.player, er_entrance[0], region)
                #entrance.is_dead_end = er_entrance[2]
                entrance.group_name = er_entrance[3]
                entrance_list.append(entrance)
                #print(f"for exit: {entrance.name} parent region: {entrance.parent_region} and connected region: {entrance.connected_region}")
                #region = self.multiworld.get_region(region_name, self.player)
                region.add_er_exits(entrance)
                # print(f"current entrance {entrance_list[len(entrance_list) - 1].name} is type: {type(entrance_list[len(entrance_list) - 1])}")
                # for exit in region.get_exits():
                #     print(f"for ER connection: {exit.name} parent region: {exit.parent_region} and connected region: {exit.connected_region}")
                    #print(f"region {region.name} has exits: {type(exit)}")
                # for exit in region.get_exits():
                #     print(f"region {region.name} has exits: {type(exit)}")



            output_connections = randomize_entrances(self.multiworld, self.player, self.random, entrance_list, True, True, minit_get_target_groups)


            for loc_name, loc_data in location_table.items():
                if not loc_data.can_create(self.multiworld, self.player):
                    continue
                region = self.multiworld.get_region(loc_data.er_region, self.player)
                new_loc = Location(self.player, loc_name, loc_data.code, region)
                if (not loc_data.show_in_spoiler):
                    new_loc.show_in_spoiler = False
                region.locations.append(new_loc)
                if loc_name == "Fight the Boss":
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(MinitItem(name = "Boss dead", classification = ItemClassification.progression, code = 60021, player = self.player))
            visualize_regions(self.multiworld.get_region("Menu", self.player), "output/regionmap.puml")
            #print(output_connections)
            #randomize_entrances(self, self, self, self, self, self, self)

        #Locked location logic from Pseudoregalia, will likely need for sword
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
        return {"slot_number": self.player,}

    def set_rules(self):
        if self.options.er_option == 0:
            minitRules = MinitRules(self)
            minitRules.set_Minit_rules()
        elif self.options.er_option == 1:
            minitRules = ER_MinitRules(self)
            minitRules.set_Minit_rules()

        if self.options.chosen_goal == 0: 
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player)
        elif self.options.chosen_goal == 1:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("ItemBrokenSword", self.player) and (minitRules.region_factory_desert(state) or minitRules.region_factory_hotel(state))
        elif self.options.chosen_goal == 2:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player) or (state.has("ItemBrokenSword", self.player) and (minitRules.region_factory_desert(state) or minitRules.region_factory_hotel(state)))
#    boss_fight = 0
#    toilet_goal = 1
#    any_goal = 2
        if (bool(self.options.starting_sword.value) == True):
            self.multiworld.local_early_items[self.player]['ItemSword'] = 1

    #difficulty settings from Pseudoregalia, won't likely need but may want to reuse
    # def set_rules(self):
    #     difficulty = self.multiworld.logic_level[self.player]
    #     if difficulty == NORMAL:
    #         PseudoregaliaNormalRules(self).set_pseudoregalia_rules()
    #     elif difficulty == HARD:
    #         PseudoregaliaHardRules(self).set_pseudoregalia_rules()
    #     elif difficulty == EXPERT:
    #         PseudoregaliaExpertRules(self).set_pseudoregalia_rules()
    #     elif difficulty == LUNATIC:
    #         PseudoregaliaLunaticRules(self).set_pseudoregalia_rules()

    def get_filler_item_name(self) -> str:
        return "HeartPiece"