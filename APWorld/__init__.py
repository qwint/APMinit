from worlds.AutoWorld import World
from BaseClasses import Region, Location, Item
from .Items import MinitItem, MinitItemData, item_table, item_frequencies
from .Locations import location_table
from .Regions import region_table
#from .options import Minit_options
from worlds.generic.Rules import add_rule, set_rule, forbid_item
from .Rules import MinitRules
from typing import Dict, Any

class MinitWorld(World):
    game = "Minit"
    required_client_version = (0, 6, 0)

    item_name_to_id = {name: data.code for name, data in item_table.items() if data.code is not None}
    location_name_to_id = {name: data.code for name, data in location_table.items() if data.code is not None}
    locked_locations = {name: data for name, data in location_table.items() if data.locked_item}
#    item_name_groups = item_groups

#    option_definitions = Minit_options

    def create_item(self, name: str) -> MinitItem:
        data = item_table[name]
        return MinitItem(name, data.classification, data.code, self.player)

    def create_items(self):
        for item_name, item_data in item_table.items():
            if (item_data.code and item_data.can_create(self.multiworld, self.player)):
                if (item_name in item_frequencies):
                    for count in range(item_frequencies[item_name]):
                        self.multiworld.itempool.append(Item(item_name,
                                                             item_data.classification,
                                                             item_data.code,
                                                             self.player))
                else:
                    self.multiworld.itempool.append(Item(item_name,
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

        for region_name, exit_list in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_exits(exit_list)

        #Locked location logic from Pseudoregalia, will likely need for sword
        # # Place locked locations.
        # for location_name, location_data in self.locked_locations.items():
        #     if not location_data.can_create(self.multiworld, self.player):
        #         continue

        #     # Doing this really stupidly because breaker's locking will change after logic rework is done
        #     if location_name == "Dilapidated Dungeon - Dream Breaker":
        #         if bool(self.multiworld.progressive_breaker[self.player]):
        #             locked_item = self.create_item("Progressive Dream Breaker")
        #             self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)
        #             continue

        #     locked_item = self.create_item(location_table[location_name].locked_item)
        #     self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {"slot_number": self.player,}

    def set_rules(self):
        MinitRules.set_Minit_rules(self)

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