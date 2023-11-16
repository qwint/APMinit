from BaseClasses import CollectionState
from typing import Dict, Set, Callable, TYPE_CHECKING
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
            "lighthouse land -> lighthouse water": lambda state:
                state.has("ItemSwim", self.player),
            "boat land -> boat water": lambda state:
                state.has("ItemSwim", self.player),
            "sword main -> sword bushes": lambda state:
                self.has_sword(state),
            "sword main -> sword water": lambda state:
                state.has("ItemSwim", self.player),
            "2crab land -> 2crab water": lambda state:
                state.has("ItemSwim", self.player),
            "2crab land -> 2crab tree exit": lambda state:
                state.has("ItemGlove", self.player),
            "dolphin land -> dolphin water": lambda state:
                state.has("ItemSwim", self.player),
            "dolphin land -> dolphin bushes": lambda state:
                self.has_sword(state),
            "desert beach land -> desert beach water": lambda state:
                state.has("ItemSwim", self.player),
            "coffee shop outside -> coffee shop pot stairs": lambda state:
                self.has_sword(state),
            "coffee shop outside -> coffee shop water": lambda state:
                state.has("ItemSwim", self.player),
            "coffee shop upper beach -> coffee shop water": lambda state:
                state.has("ItemSwim", self.player),
            "plant main -> plant bushes": lambda state:
                self.has_sword(state),
            "dog house west -> dog house river": lambda state:
                state.has("ItemSwim", self.player),
            "dog house river -> dog house east": lambda state:
                state.has("ItemSwim", self.player),
            "dog house west -> dog house bushes": lambda state:
                self.has_sword(state),
            "quicksand main -> quicksand left tree": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "quicksand main -> quicksand right tree": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "boattree main -> boattree box": lambda state:
                self.can_passBoxes(state),
            "boattree main -> boattree river": lambda state:
                state.has("ItemSwim", self.player),
            "camera river south -> camera river north": lambda state:
                self.has_sword(state) and state.has("ItemThrow", self.player),
            "camera river south -> camera river wet": lambda state:
                state.has("ItemSwim", self.player),
            "camera river north -> camera river wet": lambda state:
                state.has("ItemSwim", self.player),
            "camera house outside -> camera house tree": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "3crab main -> 3crab trees": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "sewer island mainland -> sewer island water": lambda state:
                state.has("ItemSwim", self.player),
            "throwcheck land -> throwcheck water": lambda state:
                state.has("ItemSwim", self.player),
            "throwcheck land -> throwcheck box": lambda state:
                self.has_sword(state) and state.has("ItemGrinder", self.player),
                # could be a oneway with coffee but i'll think about that later
            "arena main -> arena tree north": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "arena main -> arena tree west": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "bridge switch right -> bridge switch water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge switch left -> bridge switch water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge right -> bridge water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge left -> bridge water": lambda state:
                state.has("ItemSwim", self.player),
            "bridge left -> bridge right": lambda state:
                self.has_bridge(state),  # need to confirm this works
            "mine entrance left -> mine entrance river": lambda state:
                state.has("ItemSwim", self.player),
            "factory reception main -> factory reception east": lambda state:
                state.has("ItemPressPass", self.player),
            "factory cooler west -> factory cooler east": lambda state:
                self.has_sword(state),
            "factory loading lower main -> factory loading lower shortcut": lambda state:
                self.has_sword(state) and state.has("ItemGrinder", self.player),
                # another entrance that could have one-way logic
            "shoe shop outside -> shoe shop shortcut": lambda state:
                self.has_sword(state),
            "mine entrance bombs -> mine entrance pipe": lambda state:
                self.has_sword(state) and state.has("ItemThrow", self.player),
                # this needs to be a one-way
            "mine main -> mine main box": lambda state:
                self.has_sword(state) and state.has("ItemGrinder", self.player),
            "sewer main right -> sewer main left": lambda state:
                state.has("ItemSwim", self.player),
            "sewer bat arena -> sewer bat gate": lambda state:
                self.has_sword(state),
                # this needs to be a one-way
            "grinder south -> grinder main": lambda state:
                state.has("ItemSwim", self.player),
            "grinder east -> grinder main": lambda state:
                state.has("ItemSwim", self.player),
            "factory machine generator -> factory machine catwalk": lambda state:
                self.has_sword(state),  # has hit generator
            "miner chest belts -> miner chest pipe entrance": lambda state:
                state.has("ItemSwim", self.player),
        }

        self.location_rules = {

            # Dog House
            "Dog House - ItemCoffee": lambda state: True,
            "Dog House - ItemFlashLight": lambda state: True,
            # this ignores obscure logic rn
            "Dog House - ItemKey": lambda state:
                self.has_sword(state) and self.can_passBoxes(state),
                # need to clear the plants by the boxes even with coffee
            "Dog House - ItemWateringCan": lambda state: True,
            "Dog house - ItemBoat": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "Dog House - ItemBasement": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player) and self.has_madeboat(state),
            "Dog House - ItemPressPass": lambda state: True,
            "Dog House - House Pot Coin": lambda state:
                self.has_sword(state),
            "Dog House - Sewer Island Coin": lambda state:
                self.can_openChest(state),
            "Dog House - Sewer Coin": lambda state:
                self.has_darkroom(state) and self.can_openChest(state) and state.has("ItemSwim", self.player),
            "Dog House - Land is Great Coin": lambda state:
                self.can_openChest(state),
            "Dog House - Hidden Snake Coin": lambda state:
                self.has_darkroom(state) and self.can_openChest(state),
            "Dog House - Waterfall Coin": lambda state:
                self.can_openChest(state),
            "Dog House - Treasure Island Coin": lambda state:
                state.has("ItemSwim", self.player) and self.can_openChest(state),
            "Dog House - Plant Heart": lambda state:
                state.has("ItemWateringCan", self.player),
            "Dog House - Bull Heart": lambda state:
                self.has_sword(state),
            "Dog House - Boat Tentacle": lambda state:
                self.has_sword(state) and self.has_madeboat(state),
            "Dog House - Treasure Island Tentacle": lambda state:
                self.has_sword(state) and state.has("ItemSwim", self.player),
            "Dog House - Sword Toss Tentacle": lambda state:
                self.has_sword(state) and state.has("ItemCoffee", self.player) and state.has("ItemThrow", self.player),
            "Dog House - Sewer Tentacle": lambda state:
                self.has_sword(state) and self.has_darkroom(state) and state.has("ItemSwim", self.player),

            # Desert RV
            "Desert RV - ItemThrow": lambda state:
                self.has_sword(state),
            "Desert RV - ItemShoes": lambda state:
                self.get_coins(state, 7),
            "Desert RV - ItemGlove": lambda state: True,
            "Desert RV - ItemTurboInk": lambda state:
                self.get_tentacles(state, 8) and self.has_darkroom(state),
            "Desert RV - Temple Coin": lambda state:
                self.can_openChest(state),
                # this may change if i connect the other temple puzzles
            "Desert RV - Fire Bat Coin": lambda state:
                self.can_openChest(state),
                # this may change if i connect the other temple puzzles
            "Desert RV - Truck Supplies Coin": lambda state:
                self.has_sword(state) and self.can_openChest(state),
            "Desert RV - Broken Truck": lambda state:
                self.can_openChest(state),
            "Desert RV - Quicksand Coin": lambda state:
                self.has_sword(state) and self.has_darkroom(state),
                # vanilla does require sword because the wateringcan drops while drowing in quicksand
            "Desert RV - Dumpster": lambda state:
                self.has_sword(state),
            "Desert RV - Temple Heart": lambda state:
                state.has("ItemShoes", self.player) and (state.has("ItemFlashLight", self.player)) or (self.has_darkroom(state) and bool(self.world.options.obscure.value)),
            "Desert RV - Shop Heart": lambda state:
                self.get_coins(state, 19),
            "Desert RV - Octopus Tentacle": lambda state:
                self.has_sword(state) and state.has("ItemSwim", self.player) and self.has_darkroom(state),
            "Desert RV - Beach Tentacle": lambda state:
                self.has_sword(state),

            # Hotel Room
            "Hotel Room - ItemSwim": lambda state:
                self.has_savedResidents(state),
                # praying i can make this work
            "Hotel Room - ItemGrinder": lambda state:
                state.has("ItemSwim", self.player) and state.has("ItemCoffee", self.player) and self.has_darkroom(state),
            "Hotel Room - Shrub Arena Coin": lambda state:
                self.has_sword(state),
            "Hotel Room - Miner's Chest Coin": lambda state:
                self.can_openChest(state) and self.has_darkroom(state),
            "Factory Main - Inside Truck": lambda state: True,
            "Hotel Room - Queue": lambda state: True,
            "Hotel Room - Hotel Backroom Coin": lambda state:
                self.can_passBoxes(state) and self.has_sword(state),
            "Factory Main - Drill Coin": lambda state:
                self.has_sword(state),
            "Hotel Room - Crow Heart": lambda state:
                self.can_passBoxes(state),
            "Hotel Room - Dog Heart": lambda state:
                (self.has_sword(state) and state.has("ItemGlove", self.player) and (self.can_teleport(state) or state.has("ItemSwim", self.player) or state.has("ItemShoes", self.player))) or (self.has_sword(state) and state.has("ItemGlove", self.player) and bool(self.world.options.obscure.value)),
                # untouched until i figure out a way to logic this
            "Factory Main - Cooler Tentacle": lambda state:
                self.has_sword(state),

            # Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                (self.has_sword(state) and state.has("ItemSwim", self.player) and state.has("ItemCoffee", self.player)) or (self.has_sword(state) and state.has("ItemSwim", self.player) and bool(self.world.options.obscure.value)),

            # Underground Tent
            "Underground Tent - ItemTrophy": lambda state: True,
            "Dog House - Dolphin Heart": lambda state:
                state.has("ItemWateringCan", self.player),

            # Undefined

            "Factory Main - ItemMegaSword": lambda state:
                state.has("ItemSwim", self.player) and self.has_sword(state) and state.has("ItemWateringCan", self.player) and state.has("ItemCoffee", self.player) and self.has_darkroom(state),
                # drill shortcut for swordless entry assumed
        }

    def get_coins(self, state, count: int) -> bool:
        return state.count("Coin", self.player) >= count

    def get_tentacles(self, state, count: int) -> bool:
        return state.count("Tentacle", self.player) >= count

    def total_hearts(self, state, count: int) -> bool:
        return state.count("HeartPiece", self.player) + 2 >= count

    def has_sword(self, state) -> bool:
        return state.has_any({"ItemSword", "ItemBrokenSword", "ItemMegaSword", "ProgressiveSword"}, self.player)

    def has_darkroom(self, state) -> bool:
        return state.has("ItemFlashLight", self.player) or bool(self.world.options.darkrooms.value)

    def can_passBoxes(self, state) -> bool:
        return state.has("ItemCoffee", self.player) or (self.has_sword(state) and state.has("ItemGrinder", self.player))

    def can_openChest(self, state) -> bool:
        return state.has("ItemWateringCan", self.player) or self.has_sword(state)

    # need rewrites
    def has_savedResidents(self, state) -> bool:
        # can save all the residents to access the hotel roof
        return self.has_sword(state) and state.has("ItemCoffee", self.player) and state.has("ItemGlove", self.player) and (self.has_bridge(state) or self.region_hotel_factory(state))

    def has_bridge(self, state) -> bool:
        return state.has("ItemSwim", self.player) or (self.has_darkroom(state) and state.has("ItemThrow", self.player) and self.has_sword(state))
        # this is also accessible through the factory in the case that your factory access is desert > sword + grinder and you have press pass, but those are covered by region_hotel_factory when necessary

    def has_madeboat(self, state) -> bool:
        return state.has("ItemBoat", self.player) and state.has("ItemWateringCan", self.player) and state.has("ItemGlove", self.player)
        # boatman requires both the watering trigger and having gloves trigger to be met before he can spawn, take the boatwood and repair the boat

    def can_teleport(self, state) -> bool:
        return self.has_madeboat(state) and state.has("ItemBasement", self.player) and self.has_sword(state) and state.has("ItemSwim", self.player) or state.has("ItemCoffee", self.player)

    # meaningless but currently used
    def region_factory_hotel(self, state) -> bool:
        return (self.has_sword(state) and state.has("ItemPressPass", self.player) and
                    ((self.has_darkroom(state) and state.has("ItemThrow", self.player)) or state.has("ItemSwim", self.player))) or (state.has("ItemSwim", self.player) and self.has_darkroom(state))

    def region_factory_desert(self, state) -> bool:
        return (self.has_sword(state) and state.has("ItemGrinder", self.player)) or (state.has("ItemSwim", self.player) and state.has("ItemCoffee", self.player))

    def region_hotel_factory(self, state) -> bool:
        return self.region_DesertRV(state) and self.region_factory_desert(state) and self.has_sword(state) and state.has("ItemPressPass", self.player)

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
