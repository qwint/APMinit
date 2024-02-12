from BaseClasses import CollectionState
from typing import Dict, Set, Callable, TYPE_CHECKING, List
from worlds.generic.Rules import set_rule, add_rule
from .Options import MinitGameOptions

if TYPE_CHECKING:
    from . import MinitWorld
else:
    MinitWorld = object


class ER_MinitRules:
    world: MinitWorld
    player: int
    region_rules: Dict[str, Callable[[CollectionState], bool]]

    location_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: MinitWorld) -> None:
        self.world = world
        self.player = world.player

        self.region_rules = {
            "Menu -> sword main": lambda state: True,
            "factory machine catwalk -> Boss Fight": lambda state:
                (self.has_darkroom(state, 2) and self.has_megasword(state)),
            "factory machine generator -> Boss Fight": lambda state:
                (self.has_darkroom(state, 2) and self.has_megasword(state)),
            "lighthouse land <-> lighthouse water": lambda state:
                state.has("ItemSwim", self.player),
            "boat land <-> boat water": lambda state:
                state.has("ItemSwim", self.player),
            "sword main <-> sword bushes": lambda state:
                self.has_sword(state),
            "sword main <-> sword water": lambda state:
                state.has("ItemSwim", self.player),
            "2crab land <-> 2crab water": lambda state:
                state.has("ItemSwim", self.player),
            "2crab land <-> 2crab tree exit": lambda state:
                state.has("ItemGlove", self.player),
            "dolphin land <-> dolphin water": lambda state:
                state.has("ItemSwim", self.player),
            "dolphin land <-> dolphin bushes": lambda state:
                self.has_sword(state),
            "desert beach land <-> desert beach water": lambda state:
                state.has("ItemSwim", self.player),
            "coffee shop outside <-> coffee shop pot stairs": lambda state:
                self.has_sword(state),
            "coffee shop outside <-> coffee shop water": lambda state:
                state.has("ItemSwim", self.player),
            "coffee shop outside <-> coffee shop inside": lambda state:
                True,
            "coffee shop upper beach <-> coffee shop water": lambda state:
                state.has("ItemSwim", self.player),
            "plant main <-> plant bushes": lambda state:
                self.has_sword(state),
            "dog house west <-> dog house river": lambda state:
                state.has("ItemSwim", self.player),
            "dog house west <-> dog house bushes": lambda state:
                self.has_sword(state),
            "dog house river <-> dog house east": lambda state:
                state.has("ItemSwim", self.player),
            "quicksand main <-> quicksand left tree": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
                # technically an option to not have glove and water boatguy but
                # that adds weird issues so i'll just leave it as out of logic
            "quicksand main <-> quicksand right tree": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "boattree main <-> boattree box": lambda state:
                self.can_passBoxes(state),
            "boattree main <-> boattree river": lambda state:
                state.has("ItemSwim", self.player),
            "camera river south <-> camera river north": lambda state:
                self.has_sword(state) and state.has("ItemThrow", self.player),
            "camera river south <-> camera river wet": lambda state:
                state.has("ItemSwim", self.player),
            "camera river north <-> camera river wet": lambda state:
                state.has("ItemSwim", self.player),
            "camera house outside <-> camera house tree": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "camera house outside <-> camera house inside": lambda state:
                True,
            "3crab main <-> 3crab trees": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "sewer island mainland <-> sewer island water": lambda state:
                state.has("ItemSwim", self.player),
            "throwcheck land <-> throwcheck water": lambda state:
                state.has("ItemSwim", self.player),
            "throwcheck land -> throwcheck box": lambda state:
                self.has_sword(state)
                and state.has("ItemGrinder", self.player),
            "throwcheck box -> throwcheck land": lambda state:
                self.can_passBoxes(state),
                # could be a oneway with coffee but i'll think about that later
            "arena main <-> arena tree north": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "arena main <-> arena tree west": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "bridge switch right <-> bridge switch water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge switch left <-> bridge switch water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge right <-> bridge water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge left <-> bridge water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge left <-> bridge right": lambda state:
                state.has("bridge on", self.player),  # need to confirm this works
            "mine entrance left <-> mine entrance river": lambda state:
                state.has("ItemSwim", self.player),
            "factory reception main <-> factory reception east": lambda state:
                state.has("ItemPressPass", self.player),
            "factory cooler west <-> factory cooler east": lambda state:
                self.has_sword(state),
            "factory loading lower main -> factory loading lower shortcut": lambda state:
                self.has_sword(state)
                and state.has("ItemGrinder", self.player),
            "factory loading lower shortcut -> factory loading lower main": lambda state:
                (self.has_sword(state)
                    and state.has("ItemGrinder", self.player))
                or state.has_all({"ItemSwim", "ItemCoffee"}, self.player),
                # another entrance that could have one-way logic
            "shoe shop outside <-> shoe shop shortcut": lambda state:
                self.has_sword(state),
            "mine entrance bombs -> mine entrance pipe": lambda state:
                self.has_sword(state)
                and self.has_darkroom(state, 3)
                and state.has("ItemThrow", self.player),
            "mine entrance pipe -> mine entrance bombs": lambda state:
                self.has_darkroom(state, 3)
                and state.has("bombs exploded", self.player),
                # this needs to be a one-way
            "mine main -> mine main box": lambda state:
                self.has_sword(state)
                and state.has("ItemGrinder", self.player),
            "mine main box -> mine main": lambda state:
                self.can_passBoxes(state),
            "sewer main right <-> sewer main left": lambda state:
                self.has_darkroom(state, 2)
                and state.has("ItemSwim", self.player),
            "sewer bat arena <-> sewer bat gate": lambda state:
                self.has_sword(state)
                and self.has_darkroom(state, 3),
                # this needs to be a one-way
            "grinder south <-> grinder main": lambda state:
                self.has_darkroom(state, 1)
                and state.has("ItemSwim", self.player),
            "grinder east <-> grinder main": lambda state:
                self.has_darkroom(state, 1)  # maybe 2
                and state.has("ItemSwim", self.player),
            "factory machine generator <-> factory machine catwalk": lambda state:
                state.has("generator smashed", self.player),
            "miner chest belts <-> miner chest pipe entrance": lambda state:
                self.has_darkroom(state, 3)
                and state.has("ItemSwim", self.player),

            # unrandomized doors
            "lighthouse inside <-> lighthouse land": lambda state:
                True,
            "lighthouse inside <-> lighthouse lookout": lambda state:
                True,
            "coffee shop pot stairs <-> sewer main right": lambda state:
                self.has_darkroom(state, 2),  # maybe 3
            "dog house inside <-> dog house west": lambda state:
                True,
            "dog house inside <-> dog house basement": lambda state:
                state.has("ItemBasement", self.player),
            "glove outside <-> glove inside": lambda state:
                True,
            "snake east <-> boattree east": lambda state:
                self.has_darkroom(state, 2),
            "snake east <-> boattree main": lambda state:
                self.has_darkroom(state, 2),
            "boattree river <-> waterfall cave": lambda state:
                True,
            "sewer island <-> sewer upper": lambda state:
                self.has_darkroom(state, 2),
            "hotel outside <-> hotel reception": lambda state:
                True,
            "hotel outside <-> hotel backroom": lambda state:
                True,
            "hotel reception <-> hotel room": lambda state:
                True,
            "mine entrance right <-> mine entrance pipe": lambda state:
                True,  # self.has_darkroom(state),
            "mine entrance left <-> mine entrance path": lambda state:
                self.has_darkroom(state, 2),
            "factory loading upper <-> factory snakehall": lambda state:
                True,
            "shoe shop inside <-> shoe shop outside": lambda state:
                True,
            "shoe shop inside <-> shoe shop downstairs": lambda state:
                state.has("ItemBasement", self.player),
            "temple outside <-> temple main": lambda state:
                self.has_darkroom(state, 1),
            "desert RV main <-> RV house": lambda state:
                True,
            "island house <-> Overworld": lambda state:
                True,
            "island house <-> island teleporter": lambda state:
                state.has("ItemBasement", self.player),
            "tent room main <-> underground house": lambda state:
                True,
            "factory mega entrance <-> factory central": lambda state:
                True,
            "factory mega entrance <-> megasword upper": lambda state:
                state.has("generator smashed", self.player),
            "dog house basement <-> hotel room": lambda state:
                True,
            "dog house basement <-> shoe shop downstairs": lambda state:
                True,
            "dog house basement <-> island teleporter": lambda state:
                True,
        }

        self.location_rules = {

            # Dog House
            "Dog House - ItemCoffee": lambda state:
                self.has_sword(state),
                # needs logic to kill the crabs
            "Dog House - ItemFlashLight": lambda state:
                True,
                # this ignores obscure logic rn
            "Dog House - ItemKey": lambda state:
                self.has_sword(state) and self.can_passBoxes(state),
                # need to clear the plants by the boxes even with coffee
            "Dog House - ItemWateringCan": lambda state:
                True,
            "Dog house - ItemBoat": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "Dog House - ItemBasement": lambda state:
                self.has_sword(state)
                and state.has("ItemGlove", self.player)
                and self.has_madeboat(state),
            "Dog House - ItemPressPass": lambda state:
                True,
            "Dog House - House Pot Coin": lambda state:
                self.has_sword(state),
            "Dog House - Sewer Island Coin": lambda state:
                self.can_openChest(state),
            "Dog House - Sewer Coin": lambda state:
                self.can_openChest(state)
                and self.has_darkroom(state, 2)
                and state.has("ItemSwim", self.player),
            "Dog House - Land is Great Coin": lambda state:
                self.can_openChest(state),
            "Dog House - Hidden Snake Coin": lambda state:
                self.can_openChest(state) and self.has_darkroom(state, 2),
            "Dog House - Waterfall Coin": lambda state:
                self.can_openChest(state),
            "Dog House - Treasure Island Coin": lambda state:
                self.can_openChest(state)
                and state.has("ItemSwim", self.player),
            "Dog House - Plant Heart": lambda state:
                state.has("ItemWateringCan", self.player),
            "Dog House - Bull Heart": lambda state:
                self.has_sword(state),
            "Dog House - Boat Tentacle": lambda state:
                self.has_sword(state) and self.has_madeboat(state),
            "Dog House - Treasure Island Tentacle": lambda state:
                self.has_sword(state) and state.has("ItemSwim", self.player),
            "Dog House - Sword Toss Tentacle": lambda state:
                self.has_sword(state)
                and state.has_all({"ItemCoffee", "ItemThrow"}, self.player),
            "Dog House - Sewer Tentacle": lambda state:
                self.has_sword(state) and self.has_darkroom(state, 3)
                and state.has("ItemSwim", self.player),

            # Desert RV
            "Desert RV - ItemThrow": lambda state:
                self.has_sword(state),
            "Desert RV - ItemShoes": lambda state:
                self.get_coins(state, 7),
            "Desert RV - ItemGlove": lambda state:
                True,
            "Desert RV - ItemTurboInk": lambda state:
                self.has_darkroom(state, 2) and self.get_tentacles(state, 8),
            "Desert RV - Temple Coin": lambda state:
                self.can_openChest(state),
                # this may change if i connect the other temple puzzles
            "Desert RV - Fire Bat Coin": lambda state:
                self.can_openChest(state) and self.has_darkroom(state, 2),
                # this may change if i connect the other temple puzzles
            "Desert RV - Truck Supplies Coin": lambda state:
                self.has_sword(state) and self.can_openChest(state),
            "Desert RV - Broken Truck": lambda state:
                self.can_openChest(state),
            "Desert RV - Quicksand Coin": lambda state:
                self.has_sword(state) and self.has_darkroom(state, 2),
                # vanilla does require sword because the wateringcan
                # drops while drowing in quicksand
            "Desert RV - Dumpster": lambda state:
                self.has_sword(state),
            "Desert RV - Temple Heart": lambda state:
                self.has_darkroom(state, 3)
                and state.has("ItemShoes", self.player),
            "Desert RV - Shop Heart": lambda state:
                self.get_coins(state, 19),
            "Desert RV - Octopus Tentacle": lambda state:
                self.has_sword(state)
                and self.has_darkroom(state, 3)
                and state.has("ItemSwim", self.player),
            "Desert RV - Beach Tentacle": lambda state:
                self.has_sword(state),

            # Hotel Room
            "Hotel Room - ItemSwim": lambda state:
                self.has_savedResidents(state),
                # praying i can make this work
            "Hotel Room - ItemGrinder": lambda state:
                self.has_darkroom(state, 1)
                and state.has_all({"ItemSwim", "ItemCoffee"}, self.player),
            "Hotel Room - Shrub Arena Coin": lambda state:
                self.has_sword(state),
            "Hotel Room - Miner's Chest Coin": lambda state:
                self.can_openChest(state) and self.has_darkroom(state, 3),
            "Factory Main - Inside Truck": lambda state:
                True,
            "Hotel Room - Queue": lambda state:
                True,
            "Hotel Room - Hotel Backroom Coin": lambda state:
                self.has_sword(state) and self.can_passBoxes(state),
            "Factory Main - Drill Coin": lambda state:
                self.has_sword(state),
            "Hotel Room - Crow Heart": lambda state:
                self.can_passBoxes(state),
            "Hotel Room - Dog Heart": lambda state:
                (self.has_sword(state)
                    and state.has("ItemGlove", self.player)
                    and (self.can_teleport(state)
                         or state.has_all({
                            "ItemSwim",
                            "ItemShoes"}, self.player)))
                or (self.has_sword(state)
                    and state.has("ItemGlove", self.player)
                    and bool(self.world.options.obscure)),
                # TODO - untouched until i figure out a way to logic this
            "Factory Main - Cooler Tentacle": lambda state:
                self.has_sword(state),

            # Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                self.has_sword(state)
                and (bool(self.world.options.obscure)
                     or state.has("ItemCoffee", self.player))
                and state.has("ItemSwim", self.player),

            # Underground Tent
            "Underground Tent - ItemTrophy": lambda state: True,
            "Dog House - Dolphin Heart": lambda state:
                state.has("ItemWateringCan", self.player),

            # Undefined
            "Factory Main - ItemMegaSword": lambda state:
                self.has_sword(state)
                and state.has_all({
                    "ItemWateringCan",
                    "left machine",
                    "right machine",
                    "drill smacked",  # game quirk
                    }, self.player),

            # events
            "generator smashed": lambda state:
                self.has_sword(state),
            "drill smacked": lambda state:
                self.has_sword(state),
            "swimmer saved": lambda state:
                True,
            "hostage saved": lambda state:
                self.has_sword(state),
            "wallet saved": lambda state:
                state.has("ItemCoffee", self.player),
            "ninja saved": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "bridge on": lambda state:
                self.has_sword(state),
            "bridge saved": lambda state:
                state.has("bridge on", self.player),
            "hidden saved": lambda state:
                self.can_passBoxes(state),
            "teleporter switch1": lambda state:
                self.has_sword(state),
            "teleporter switch4": lambda state:
                self.has_sword(state),
            "teleporter switch6": lambda state:
                self.has_sword(state),
            "boatguy watered": lambda state:
                state.has("ItemWateringCan", self.player),
            "left machine": lambda state:
                self.has_darkroom(state, 1)
                and state.has("ItemCoffee", self.player),
            "right machine": lambda state:
                self.has_sword(state),
        }

    def get_coins(self, state, count: int) -> bool:
        return state.has("Coin", self.player, count)

    def get_tentacles(self, state, count: int) -> bool:
        return state.has("Tentacle", self.player, count)

    def total_hearts(self, state, count: int) -> bool:
        if self.world.options.damage_boosts:
            return state.has("HeartPiece", self.player, count - 2)
        else:
            return False

    def has_sword(self, state) -> bool:
        return state.prog_items[self.player]["has_sword"] > 0

    def has_megasword(self, state) -> bool:
        if self.world.options.progressive_sword == "off":
            return state.has("ItemMegaSword", self.player)
        elif self.world.options.progressive_sword == "forward_progressive":
            return state.count("Progressive Sword", self.player) >= 3
        elif self.world.options.progressive_sword == "reverse_progressive":
            return state.count("Reverse Progressive Sword", self.player) >= 1

    def has_brokensword(self, state) -> bool:
        if self.world.options.progressive_sword == "off":
            return state.has("ItemBrokenSword", self.player)
        elif self.world.options.progressive_sword == "forward_progressive":
            return state.count("Progressive Sword", self.player) >= 1
        elif self.world.options.progressive_sword == "reverse_progressive":
            return state.count("Reverse Progressive Sword", self.player) >= 3

    def has_darkroom(self, state, value) -> bool:
        return (self.world.options.darkrooms >= value
                or state.has("ItemFlashLight", self.player))

    def can_passBoxes(self, state) -> bool:
        return ((
                    self.has_sword(state)
                    and state.has("ItemGrinder", self.player))
                or state.has("ItemCoffee", self.player))

    def can_openChest(self, state) -> bool:
        return (self.has_sword(state)
                or state.has("ItemWateringCan", self.player))

    def has_savedResidents(self, state) -> bool:
        return state.has_all({
            "swimmer saved",
            "hostage saved",
            "wallet saved",
            "ninja saved",
            "bridge saved",
            "hidden saved",
            }, self.player)

    def has_madeboat(self, state) -> bool:
        return state.has_all({
            "ItemBoat",
            "boatguy watered",
            "ItemGlove",
            }, self.player)

    def can_teleport(self, state) -> bool:
        return state.has_all({
                "teleporter switch1",
                "teleporter switch4",
                "teleporter switch6",
            }, self.player)

    def rev(self, e_name: str) -> List[str]:
        e_list = e_name.split(" -> ")
        if len(e_list) == 2:
            return [f"{e_list[1]} <-> {e_list[0]}", f"{e_list[0]} <-> {e_list[1]}"]
        else:
            return ["", ""]

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld
        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
                else:
                    twoWayName = self.rev(entrance.name)
                    if twoWayName[0] in self.region_rules:
                        set_rule(
                            entrance,
                            self.region_rules[twoWayName[0]]
                            )
                    elif twoWayName[1] in self.region_rules:
                        set_rule(
                            entrance,
                            self.region_rules[twoWayName[1]]
                            )
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
