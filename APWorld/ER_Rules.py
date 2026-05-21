from typing import TYPE_CHECKING
from rule_builder.rules import And, CanReachRegion, False_, Has, HasAll, HasAny, Or, True_
from . import RuleUtils

if TYPE_CHECKING:
    from . import MinitWorld
else:
    MinitWorld = object


swim_helper = Has("ItemSwim")
darkroom1_helper = RuleUtils.has_darkroom1
darkroom2_helper = RuleUtils.has_darkroom2
darkroom3_helper = RuleUtils.has_darkroom3
sword_helper = Has("has_sword")
wateringcan_helper = Has("ItemWateringCan")
presspass_helper = Has("ItemPressPass")
basement_helper = Has("ItemBasement")
tree_helper = Has("has_sword") & Has("ItemGlove")
chest_helper = RuleUtils.can_open_chest
box_helper = RuleUtils.can_pass_boxes
teleport_helper = HasAll("teleporter switch1", "teleporter switch4", "teleporter switch6")


region_rules = {
    # "Menu -> sword main": True_(),
    "factory machine catwalk -> Boss Fight": darkroom2_helper & RuleUtils.has_megasword,
    "Boss Fight -> factory machine catwalk": False_(),
    "factory machine generator -> Boss Fight": darkroom2_helper & RuleUtils.has_megasword,
    "Boss Fight -> factory machine generator": False_(),
    "2crab tree exit <-> 2crab tile": tree_helper | swim_helper,
    "boat tile -> Overworld island shack": HasAll("ItemBoat", "boatguy watered", "ItemGlove"),
    "Overworld island shack -> boat tile": False_(),
    # "coffee shop outside <-> coffee shop inside": True_(),
    "quicksand left tree <-> quicksand main":  tree_helper,
    # technically an option to not have glove and water boatguy but
    # that adds weird issues so i'll just leave it as out of logic
    "quicksand right tree <-> quicksand main":  tree_helper,
    "factory drill <-> quicksand main": Has("drill smacked"),
    "boattree box <-> boattree main":  box_helper,
    "camera river south -> camera river north": sword_helper & Has("ItemThrow"),
    "camera river north -> camera river south": Has("has_sword") | RuleUtils.obscure_enabled,
    # obscure: requires nothing, Push archers into poison river
    "camera house tree <-> camera house outside":  tree_helper,
    # "camera house outside <-> camera house inside": True_(),
    "3crab trees <-> 3crab main":  tree_helper,
    "throwcheck tile -> throwcheck box": sword_helper & Has("ItemGrinder"),
    # TODO: this currently allows for throw check to be in logic without being possible.
    # It might make sense to make going this way out of logic to fix that.
    "throwcheck box -> throwcheck tile":  box_helper,
    # could be a oneway with coffee but i'll think about that later
    "arena tree north <-> arena tile":  tree_helper,
    "arena tree west <-> arena tile":  tree_helper,
    "bridge left <-> bridge right": Has("bridge on"),  # need to confirm this works
    "factory loading lower main <-> factory loading lower shortcut": sword_helper & Has("ItemGrinder"),
    # damage boosting out of logic
    "mine entrance pipe <-> mine entrance bombs": darkroom3_helper & Has("bombs exploded"),
    "mine main -> mine main box": sword_helper & Has("ItemGrinder"),
    "mine main box -> mine main":  box_helper,
    "sewer main right north <-> sewer main":  darkroom2_helper,
    "sewer main left <-> sewer main": darkroom2_helper & swim_helper,
    "sewer bat arena -> sewer bat gate": sword_helper & darkroom3_helper,
    # this needs to be a one-way as the bats respawn
    "sewer bat gate -> sewer bat arena": False_(),
    "grinder south": darkroom1_helper & swim_helper,
    "grinder east": darkroom1_helper,  # maybe 2 & swim_helper,
    "factory machine generator <-> factory machine catwalk": Has("generator smashed"),
    "miner chest pipe entrance <-> miner chest tile": darkroom3_helper & swim_helper,
    # TODO: Better damage boosting logic
    # This is the only instance of allowed damage boosting. The reason for this is because this path is only possible
    # through damage boosting and is a path that is required to be taken, through damage boosting, in vanilla.
    # Anyway, it's possible for this to cause logic problems if it needs to be passed through multiple times in one run.
    # For example, if you needed to pass through here to get to the set of 3 crabs and then needed to travel back
    # through here before you could claim the coffee location, it may be impossible due to the damage taken

    # unrandomized doors
    "lighthouse inside <-> lighthouse":  Has("ItemKey"),
    "lighthouse lookout -> lighthouse": False_(),
    "lighthouse -> lighthouse lookout": Or(False_(), Has("ItemSwim") & RuleUtils.obscure_enabled),
    # obscure: you can swim and grab it from beneath
    # "lighthouse inside -> lighthouse lookout": True_(),
    "lighthouse lookout -> lighthouse inside": False_(),
    "coffee shop pot stairs <-> sewer main":  darkroom2_helper,  # maybe 3
    # "dog house inside <-> dog house west": True_(),
    # "glove outside <-> glove inside": True_(),
    "boattree main <-> waterfall cave":  swim_helper,
    # "hotel outside <-> hotel reception": True_(),
    # "hotel outside <-> hotel backroom": True_(),
    # "hotel reception <-> hotel room": True_(),
    # "mine entrance right <-> mine entrance pipe": True_(),
    # "factory loading upper <-> factory snakehall": True_(),
    # "shoe shop inside <-> shoe shop outside": True_(),
    # "desert RV main <-> RV house": True_(),
    "Overworld treasure island <-> Overworld island shack": Has("ItemSwim") & RuleUtils.obscure_enabled,
    # obscure: you can swim accross, Bait the sharks
    "island house -> Overworld island shack": True_(),
    "Overworld island shack -> island house": sword_helper,
    "island house -> island teleporter": basement_helper & darkroom1_helper,
    "island teleporter -> island house": darkroom1_helper,
    "island teleporter east":  darkroom1_helper,
    # "tent room main <-> underground house": True_(),
    # "factory mega entrance <-> factory central": True_(),
    "factory mega entrance <-> megasword upper": Has("generator smashed") & darkroom1_helper,
    "factory central south <-> factory central": Has("generator smashed"),
    "dog house basement <-> hotel room":  teleport_helper & CanReachRegion("hotel room"),
    "dog house basement <-> shoe shop downstairs":  teleport_helper & CanReachRegion("shoe shop downstairs"),
    "temple coin test north": (
        CanReachRegion("dog house inside")
        & CanReachRegion("RV house")
        & CanReachRegion("hotel room")
        & CanReachRegion("island house")
        & darkroom3_helper
        ),
    "temple coin test south": (
        CanReachRegion("dog house inside")
        & CanReachRegion("RV house")
        & CanReachRegion("hotel room")
        & CanReachRegion("island house")
        & darkroom3_helper
        ),

    # # only swims
    "lighthouse water upper west":  swim_helper,
    "lighthouse water upper north":  swim_helper,
    "lighthouse water upper east":  swim_helper,
    "lighthouse water lower west":  swim_helper,
    "lighthouse water lower south":  swim_helper,
    "lighthouse water lower east":  swim_helper,
    "boat water south":  swim_helper,
    "boat water east":  swim_helper,
    "boat water north":  swim_helper,
    "boat water west":  swim_helper,
    "sword east <-> sword water":  swim_helper,
    "2crab land north river":  swim_helper,
    "2crab water east":  swim_helper,
    "2crab water south":  swim_helper,
    "2crab water west":  swim_helper,
    "dolphin water east":  swim_helper,
    "dolphin water south":  swim_helper,
    "dolphin water west":  swim_helper,
    "desert beach water south":  swim_helper,
    "desert beach water west":  swim_helper,
    "coffee shop water north":  swim_helper,
    "coffee shop water west":  swim_helper,
    "coffee shop water south":  swim_helper,
    "coffee shop upper beach -> coffee shop outside": swim_helper,
    "coffee shop outside -> coffee shop upper beach":  swim_helper | And(
        Has("ItemCoffee"),
        Has("has_sword") | RuleUtils.obscure_enabled
        # obscure: coffee without sword, Coffee shop to upper beach without breaking pot
        ),

    "above lighthouse water north":  swim_helper,
    "above lighthouse water east upper":  swim_helper,
    "above lighthouse water east lower":  swim_helper,
    "above lighthouse water south":  swim_helper,
    "above lighthouse water west":  swim_helper,

    "dog house west <-> dog house east":  swim_helper,
    "dog house river north":  swim_helper,
    "dog house river south":  swim_helper,

    "boattree river south":  swim_helper,
    "3crab north water north":  swim_helper,
    "3crab north water west":  swim_helper,
    "3crab south water west":  swim_helper,
    "3crab south water south":  swim_helper,
    "sewer island water north":  swim_helper,
    "sewer island water south":  swim_helper,
    "sewer island water west":  swim_helper,
    "throwcheck water south":  swim_helper,
    "throwcheck water west":  swim_helper,
    "Overworld wet06": swim_helper,
    "bridge switch left <-> bridge switch right":  False_(), # damage boosting is out of logic

    # # toxic waters

    "sewer island tile -> toxic waters":  swim_helper & sword_helper,
    "toxic waters -> sewer island tile": False_(),
    "camera river south -> camera river wet": swim_helper,
    "camera river wet -> camera river south": False_(),
    "mine entrance left -> toxic waters": swim_helper,
    "toxic waters -> mine entrance left": False_(),
    "bridge left -> toxic waters": swim_helper,
    "toxic waters -> bridge left": False_(),
    "bridge switch left -> toxic waters": swim_helper,
    "toxic waters -> bridge switch left": False_(),

    # This logic is here so that the generic entrance randomizer doesn't crash randomizing toxic water connections
    # with eachother when they aren't logically useful.
    # This logic says that you can enter the toxic waters, but you cannot exit, making it useless for logic.


    "temple octopus north": swim_helper & darkroom3_helper,

    # # darkroom only
    "submarine east":  darkroom1_helper,
    "submarine west":  darkroom1_helper,
    "teleporter maze west":  darkroom1_helper,
    # not doing it's job, but it feels unnecessary anyway:
    # It's still in logic to come from the west without flashlight for some reason
    "mine main north":  darkroom1_helper,
    "mine main west upper": darkroom1_helper,
    # so that regions don't have to be added to enforce darkroom rules on mine main north and mine main west lower
    "mine main west lower":  darkroom1_helper,
    "mine main box": darkroom1_helper,
    # so that regions don't have to be added to enforce darkroom rules on mine main north and mine main west lower
    "factory switch test west":  darkroom1_helper,
    "factory switch test south":  darkroom1_helper,
    "dog house basement <-> island teleporter": (
        teleport_helper & CanReachRegion("island teleporter") & darkroom1_helper),

    "snake east <-> boattree east":  darkroom2_helper,
    "snake east <-> boattree main":  darkroom2_helper,
    "snake east path":  darkroom2_helper,
    "sewer island <-> sewer upper":  darkroom2_helper,
    "temple outside <-> temple main":  darkroom2_helper,
    "mine entrance left <-> mine entrance path":  darkroom2_helper,
    "tent room pipe I right":  darkroom2_helper,
    "tent room pipe I left":  darkroom2_helper,
    "tent room main right":  darkroom2_helper,  # changed from 1 to 2 since you'd always travel across
    "tent room main left":  darkroom2_helper,

    "tent room pipe O":  darkroom3_helper,
    "temple octopus main": darkroom3_helper,
    "miner chest pipe L south":  darkroom3_helper,
    "miner chest pipe L west":  darkroom3_helper,
    "trophy pipe hall right":  darkroom3_helper,
    "trophy pipe hall left":  darkroom3_helper,
    "trophy maze lower main north right":  darkroom3_helper,
    "trophy maze lower main north left":  darkroom3_helper,
    "trophy maze lower main east right":  darkroom3_helper,  # east upper
    "trophy maze lower main east left":  darkroom3_helper,  # east lower
    "trophy maze lower hall left":  darkroom3_helper,
    "trophy maze lower hall right":  darkroom3_helper,
    "trophy maze upper main right":  darkroom3_helper,
    "trophy maze upper main left":  darkroom3_helper,
    "trophy maze upper hall south":  darkroom3_helper,
    "trophy maze upper hall west":  darkroom3_helper,

    # # sword
    "sword east <-> sword west": sword_helper,
    "dolphin bushes":  sword_helper,
    "dog house bushes <-> dog house west":  sword_helper,
    "coffee shop outside -> coffee shop pot stairs": Or(
        sword_helper,
        Has("ItemShoes") & RuleUtils.obscure_enabled
        # Shoes to skip breaking the pot
        ),
    "coffee shop pot stairs -> coffee shop outside": True_(),
    "plant bushes <-> plant tile":  sword_helper,
    "shoe shop shortcut <-> shoe shop outside":  sword_helper,
    "factory cooler west <-> factory cooler tile":  sword_helper | (Has("ItemShoes") & RuleUtils.obscure_enabled),
    # obscure: shoes, Glitch through with precision
    "temple main north <-> temple main": sword_helper,

    # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time
    "temple main east <-> temple main":  wateringcan_helper,
    "temple firebat test east": wateringcan_helper & darkroom2_helper,
    "temple firebat test west": wateringcan_helper & darkroom2_helper,
    # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time

    "dog house inside -> dog house basement":  basement_helper,
    "dog house basement -> dog house inside": True_(),
    "shoe shop inside -> shoe shop downstairs":  basement_helper,
    "shoe shop downstairs -> shoe shop inside": True_(),

    "factory reception east <-> factory reception tile":  presspass_helper,
}

location_rules = {
    # Dog House
    "Dog House - ItemCoffee": sword_helper & CanReachRegion("2crab tile") & CanReachRegion("3crab main"),
    # "Dog House - ItemFlashLight": True_(),
    "Dog House - ItemKey": sword_helper & box_helper,
    # need to clear the plants by the boxes even with coffee
    # "Dog House - ItemWateringCan": True_(),
    "Dog house - ItemBoat":  tree_helper,
    "Dog House - ItemBasement": tree_helper,
    # "Dog House - ItemPressPass": True_(),
    "Dog House - House Pot Coin":  sword_helper,
    "Dog House - Sewer Island Coin":  chest_helper,
    "Dog House - Sewer Coin": chest_helper & darkroom2_helper & swim_helper,
    "Dog House - Land is Great Coin":  chest_helper,
    "Dog House - Hidden Snake Coin": chest_helper & darkroom3_helper,
    "Dog House - Waterfall Coin": chest_helper & darkroom1_helper,
    "Dog House - Treasure Island Coin": chest_helper & swim_helper,
    "Dog House - Plant Heart":  wateringcan_helper,
    "Dog House - Bull Heart":  sword_helper,
    "Dog House - Boat Tentacle": sword_helper & HasAll("ItemBoat", "boatguy watered", "ItemGlove"),
    "Dog House - Treasure Island Tentacle": sword_helper & swim_helper,
    "Dog House - Sword Toss Tentacle": sword_helper & HasAll("ItemCoffee", "ItemThrow"),
    "Dog House - Sewer Tentacle": sword_helper & darkroom3_helper & swim_helper,

    # Desert RV
    "Desert RV - ItemThrow":  sword_helper,
    "Desert RV - ItemShoes": Has("Coin", 7),
    "Desert RV - ItemGlove":  darkroom1_helper,
    "Desert RV - ItemTurboInk": darkroom3_helper & Has("Tentacle", 8),
    "Desert RV - Temple Coin": sword_helper & darkroom2_helper,
    # this may change if i connect the other temple puzzles
    "Desert RV - Fire Bat Coin": chest_helper & darkroom2_helper,
    # this may change if i connect the other temple puzzles
    "Desert RV - Truck Supplies Coin": sword_helper,
    "Desert RV - Broken Truck":  chest_helper,
    "Desert RV - Quicksand Coin": sword_helper & darkroom2_helper,
    # vanilla does require sword because the wateringcan
    # drops while drowning in quicksand
    "Desert RV - Dumpster":  sword_helper,
    "Desert RV - Temple Heart": darkroom3_helper & Has("ItemShoes"),
    "Desert RV - Shop Heart": Has("Coin", 19),
    "Desert RV - Octopus Tentacle": sword_helper & darkroom3_helper & swim_helper,
    "Desert RV - Beach Tentacle":  sword_helper,

    # Hotel Room
    "Hotel Room - ItemSwim": HasAll(
        "swimmer saved", "hostage saved", "wallet saved", "ninja saved", "bridge saved", "hidden saved"),
    # praying i can make this work
    "Hotel Room - ItemGrinder": darkroom2_helper & HasAll("ItemSwim", "ItemCoffee"),
    "Hotel Room - Shrub Arena Coin":  sword_helper,
    "Hotel Room - Miner's Chest Coin": chest_helper & darkroom3_helper,
    # "Factory Main - Inside Truck":  True,
    # "Hotel Room - Queue": True_(),
    "Hotel Room - Hotel Backroom Coin": sword_helper & box_helper,
    # sword is not actually necessary due to non-vanilla behaviors with the stuff that gets put into the pot.
    "Factory Main - Drill Coin":  sword_helper,
    "Hotel Room - Crow Heart":  box_helper,
    "Hotel Room - Dog Heart": CanReachRegion("dog house inside"),
    "Factory Main - Cooler Tentacle":  sword_helper,

    # Island Shack
    "Island Shack - Teleporter Tentacle": (
        sword_helper
        & darkroom1_helper
        & (Has("ItemCoffee") | RuleUtils.obscure_enabled)
        & swim_helper
        ),
    # obscure: Coffee not required

    # Underground Tent
    "Underground Tent - ItemTrophy":  darkroom1_helper,
    "Dog House - Dolphin Heart":  wateringcan_helper,
    # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time

    # Undefined
    "Factory Main - ItemMegaSword": sword_helper & HasAll("ItemWateringCan", "left machine", "right machine"),

    # events
    "generator smashed":  sword_helper,
    "drill smacked":  sword_helper,
    # "swimmer saved":
    #     True,
    "hostage saved":  sword_helper,
    "wallet saved": Has("ItemCoffee"),
    "ninja saved":  tree_helper,
    "bridge on":  sword_helper,
    "bridge saved": Has("bridge on"),
    "hidden saved":  box_helper,
    "teleporter switch1": sword_helper & darkroom3_helper,
    "teleporter switch4":  sword_helper & (Has("ItemCoffee") | swim_helper),
    "teleporter switch6":  sword_helper & (Has("ItemCoffee") | swim_helper),
    "boatguy watered":  wateringcan_helper,
    # TODO: fix logical issues with not being able to carry a sword and a watering can at the same time
    "left machine": darkroom1_helper & HasAll("ItemSwim", "ItemCoffee"),
    "right machine": darkroom1_helper & sword_helper,
    "bombs exploded": sword_helper & Has("ItemThrow") & darkroom3_helper,
}


class ER_MinitRules:
    world: MinitWorld

    def __init__(self, world: MinitWorld) -> None:
        self.world = world

    def rev(self, e_name: str) -> (str, str):
        e_list = e_name.split(" -> ")
        if len(e_list) == 2:
            return f"{e_list[1]} <-> {e_list[0]}", f"{e_list[0]} <-> {e_list[1]}"
        else:
            return "", ""

    def set_Minit_rules(self) -> None:
        for region in self.world.get_regions():
            for entrance in region.entrances:
                if entrance.name in region_rules:
                    self.world.set_rule(entrance, region_rules[entrance.name])
                else:
                    left_name, right_name = self.rev(entrance.name)
                    if left_name in region_rules:
                        self.world.set_rule(
                            entrance,
                            region_rules[left_name]
                            )
                    elif right_name in region_rules:
                        self.world.set_rule(
                            entrance,
                            region_rules[right_name]
                            )
            for location in region.locations:
                if location.name in location_rules:
                    self.world.set_rule(location, location_rules[location.name])
