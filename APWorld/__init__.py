from worlds.AutoWorld import World
from BaseClasses import Region, Location, Item, ItemClassification
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
#TODO - confirm upgraded swords do the upgraded damage
#TODO - figure out how to add tests and test for
            #confirm a sword or swim is in the first two checks
            #confirm prog balancing settings (min/loc/items) work
            #confirm the options are working as intended (when added)

#misc game mod TODOs
#TODO - pull all required game mods out and reapply to clean up patch file

#add options
#TODO - sword is sword option
#TODO - add a darkroom option to ignore flashlight req
#TODO - figure out how to progressive sword
#TODO - figure out how to add alt goal (flush broken sword)
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
#TODO - add more routes for Dog Heart
#TODO - add swim to the island shack door requirement (may softlock players without obscure logic, confirm the swim back is easier)
#TODO       if above then add swim as an option for getting 1/4 of temple coin

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
        minitRules = MinitRules(self)
        minitRules.set_Minit_rules()
        if self.options.chosen_goal == 0: 
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player)
        elif self.options.chosen_goal == 1:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("ItemBrokenSword", self.player) and (self.region_factory_desert(state) or self.region_factory_hotel(state))
        elif self.options.chosen_goal == 2:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player) or (state.has("ItemBrokenSword", self.player) and (self.region_factory_desert(state) or self.region_factory_hotel(state)))
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