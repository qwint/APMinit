from BaseClasses import CollectionState
from typing import Dict, Callable, TYPE_CHECKING  # Set
from worlds.generic.Rules import set_rule  # add_rule
# from .Options import MinitGameOptions
from . import RuleUtils

if TYPE_CHECKING:
    from . import MinitWorld
else:
    MinitWorld = object


class MinitRules:
    world: MinitWorld
    player: int
    region_rules: Dict[str, Callable[[CollectionState], bool]]

    location_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: MinitWorld) -> None:
        self.world = world
        self.player = world.player

        self.region_rules = {
            "Menu -> Dog House": lambda state:
                True,
            "Dog House -> Island Shack": lambda state:
                (bool(self.world.options.obscure)
                 and state.has("ItemSwim", self.player))
                or (state.has_all({
                    "ItemBoat",
                    "boatguy watered",
                    "ItemGlove",
                    }, self.player)),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Dog House -> Desert RV": lambda state:
                (state.has("has_sword", self.player) and
                    (RuleUtils.has_darkroom(self.world, state, 2)
                     or state.has("ItemGlove", self.player)))
                or state.has("ItemSwim", self.player),
            "Dog House -> Hotel Room": lambda state:
                (state.has("has_sword", self.player)
                 and state.has("ItemGlove", self.player))
                or state.has("ItemSwim", self.player),
            "Island Shack -> Basement": lambda state:
                state.has("has_sword", self.player)
                and state.has("ItemBasement", self.player),
            "Desert RV -> Factory Main": lambda state:
                state.has("has_sword", self.player)
                and (state.has("ItemGrinder", self.player)
                     or state.has_all({
                        "ItemSwim",
                        "ItemCoffee"
                        }, self.player)),
            "Hotel Room -> Underground Tent": lambda state:
                state.has("has_sword", self.player)
                and RuleUtils.has_darkroom(self.world, state, 3)
                and state.has("ItemGrinder", self.player),
            "Hotel Room -> Factory Main": lambda state:
                (RuleUtils.has_darkroom(self.world, state, 2)
                    and state.has("ItemSwim", self.player))
                or (
                    state.has("has_sword", self.player)
                    and state.has("ItemPressPass", self.player)
                    and ((
                            RuleUtils.has_darkroom(self.world, state, 3)
                            and state.has("ItemThrow", self.player))
                         or state.has("ItemSwim", self.player)
                         )
                ),
            "Factory Main -> Boss Fight": lambda state:
                RuleUtils.has_darkroom(self.world, state, 2)
                and RuleUtils.has_megasword(self.world, state),
            "Factory Main -> Hotel Room": lambda state:
                self.factory_to_hotel_backtrack(state),
        }

        self.location_rules = {

            # Dog House
            "Dog House - ItemCoffee": lambda state:
                state.has("has_sword", self.player),
            "Dog House - ItemFlashLight": lambda state:
                (bool(self.world.options.obscure)
                    and state.has("ItemSwim", self.player))
                or ((
                     state.has("has_sword", self.player)
                     or state.has("ItemSwim", self.player))
                    and state.has("ItemKey", self.player)),
                # obscure: you can swim behind the lighthouse
                # - and pick up the item
            "Dog House - ItemKey": lambda state:
                state.has("has_sword", self.player) and RuleUtils.can_passBoxes(self.world, state),
                # can swim past the plants,
                # but need to clear the plants by the boxes
            "Dog House - ItemWateringCan": lambda state:
                state.has("has_sword", self.player),
            "Dog house - ItemBoat": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player),
            "Dog House - ItemBasement": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player)
                and ((bool(self.world.options.obscure)
                      and state.has("ItemSwim", self.player))
                     or state.has_all({
                        "ItemBoat",
                        "boatguy watered",
                        "ItemGlove",
                        }, self.player)),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Dog House - ItemPressPass": lambda state:
                (
                    (RuleUtils.can_passBoxes(self.world, state)
                        and ((state.has("has_sword", self.player)
                              and state.has("ItemThrow", self.player))
                             or state.has("ItemSwim", self.player)))
                    or (state.has("has_sword", self.player)
                        and state.can_reach("Hotel Room", player=self.player)
                        and (state.has_all({
                                "ItemGrinder",
                                "ItemGlove"
                                }, self.player))
                        or (RuleUtils.total_hearts(self.world, state, 4)
                            and state.has("ItemSwim", self.player))))
                or (RuleUtils.total_hearts(self.world, state, 7)
                    and bool(self.world.options.obscure)
                    and state.can_reach("Hotel Room", player=self.player)
                    and state.has("ItemSwim", self.player)),
                # obscure: you can, with clean movement and damage tanks,
                # - swim from the factory bridge to press pass house
                # - without any other items
            "Dog House - House Pot Coin": lambda state:
                state.has("has_sword", self.player),
            "Dog House - Sewer Island Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.world, state, 3)
                and RuleUtils.can_openChest(self.world, state),
            "Dog House - Sewer Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.world, state, 3)
                and RuleUtils.can_openChest(self.world, state)
                and state.has("ItemSwim", self.player),
            "Dog House - Land is Great Coin": lambda state:
                RuleUtils.can_openChest(self.world, state)
                and ((
                        state.has("has_sword", self.player)
                        and state.has("ItemCoffee", self.player))
                     or state.has("ItemSwim", self.player)),
            "Dog House - Hidden Snake Coin": lambda state:
                (state.has("has_sword", self.player) or state.has("ItemSwim", self.player))
                and RuleUtils.has_darkroom(self.world, state, 2) and RuleUtils.can_openChest(self.world, state),
            "Dog House - Waterfall Coin": lambda state:
                RuleUtils.can_openChest(self.world, state)
                and state.has("ItemSwim", self.player),
            "Dog House - Treasure Island Coin": lambda state:
                RuleUtils.can_openChest(self.world, state)
                and state.has("ItemSwim", self.player),
            "Dog House - Plant Heart": lambda state:
                state.has("ItemWateringCan", self.player),
            "Dog House - Bull Heart": lambda state:
                state.has("has_sword", self.player)
                and (state.can_reach("Desert RV", player=self.player)
                     or RuleUtils.has_darkroom(self.world, state, 2)),
            "Dog House - Boat Tentacle": lambda state:
                state.has("has_sword", self.player)
                and state.has_all({
                    "ItemBoat",
                    "boatguy watered",
                    "ItemGlove",
                    }, self.player),
            "Dog House - Treasure Island Tentacle": lambda state:
                state.has("has_sword", self.player) and state.has("ItemSwim", self.player),
            "Dog House - Sword Toss Tentacle": lambda state:
                state.has("has_sword", self.player)
                and state.has_all({
                    "ItemCoffee",
                    "ItemThrow",
                    "ItemGlove",
                    }, self.player),
            "Dog House - Sewer Tentacle": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.world, state, 3)
                and state.has("ItemSwim", self.player),
            "Dog House - Dolphin Heart": lambda state:
                state.has("ItemWateringCan", self.player),
                # Non Vanilla Location: water the dolphin NPC
                # -  south of the watering can location

            # Desert RV
            "Desert RV - ItemThrow": lambda state:
                state.has("has_sword", self.player),
            "Desert RV - ItemShoes": lambda state:
                state.has("Coin", self.player, 7),
            "Desert RV - ItemGlove": lambda state:
                (state.has("has_sword", self.player)
                    and state.has("ItemGlove", self.player))
                or state.has_any({
                    "ItemWateringCan",
                    "ItemSwim",
                    }, self.player),
            "Desert RV - ItemTurboInk": lambda state:
                RuleUtils.has_darkroom(self.world, state, 2) and state.has("Tentacle", self.player, 8),
            "Desert RV - Temple Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.world, state, 2)
                and ((
                        state.can_reach("Hotel Room", player=self.player)
                        and state.has_all({
                            "teleporter switch1",
                            "teleporter switch4",
                            "teleporter switch6",
                            "ItemBasement",
                            }, self.player))
                     or (self.world.options.obscure
                         and state.has("ItemSwim", self.player)
                         # sword+darkroom+swim should cover the hotel -> temple route
                         )
                     ),
                # item region implies desert rv access, can teleport implies
                # - island shack access, existing implies dog house access,
                # - only need to check hotel room access
            "Desert RV - Fire Bat Coin": lambda state:
                RuleUtils.has_darkroom(self.world, state, 1) and RuleUtils.can_openChest(self.world, state)
                and state.has("ItemWateringCan", self.player),
            "Desert RV - Truck Supplies Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.can_openChest(self.world, state),
            "Desert RV - Broken Truck": lambda state:
                RuleUtils.can_openChest(self.world, state),
            "Desert RV - Quicksand Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.world, state, 2),
                # vanilla does require sword because the wateringcan drops
                # - while drowing in quicksand
            "Desert RV - Dumpster": lambda state:
                state.has("has_sword", self.player),
            "Desert RV - Temple Heart": lambda state:
                RuleUtils.has_darkroom(self.world, state, 3)
                and state.has("ItemShoes", self.player),
            "Desert RV - Shop Heart": lambda state:
                state.has("ItemBasement", self.player)
                and state.has("Coin", self.player, 19),
            "Desert RV - Octopus Tentacle": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.world, state, 2)
                and state.has("ItemSwim", self.player),
            "Desert RV - Beach Tentacle": lambda state:
                state.has("has_sword", self.player),
                # redundant rules as swim gets us to the right region anyways
                # or (self.region_DogHouse(state)
                #     and state.has("has_sword", self.player)
                #     and state.has("ItemSwim", self.player)),

            # Hotel Room
            "Hotel Room - ItemSwim": lambda state:
                state.has_all({
                    "swimmer saved",
                    "hostage saved",
                    "wallet saved",
                    "ninja saved",
                    "bridge saved",
                    "hidden saved",
                    }, self.player),
            "Hotel Room - ItemGrinder": lambda state:
                RuleUtils.has_darkroom(self.world, state, 2)
                and state.has_all({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player),
            "Hotel Room - Shrub Arena Coin": lambda state:
                state.has("has_sword", self.player),
            "Hotel Room - Miner's Chest Coin": lambda state:
                state.has("has_sword", self.player) and RuleUtils.has_darkroom(self.world, state, 3)
                and RuleUtils.can_openChest(self.world, state)
                and state.has("ItemGrinder", self.player),
            "Factory Main - Inside Truck": lambda state:
                True,
            "Hotel Room - Queue": lambda state:
                self.factory_to_hotel_backtrack(state)
                or state.has_any({"ItemSwim", "bridge on"}, self.player),
            "Hotel Room - Hotel Backroom Coin": lambda state:
                RuleUtils.can_passBoxes(self.world, state) and state.has("has_sword", self.player),
            "Factory Main - Drill Coin": lambda state:
                state.has("has_sword", self.player),
            "Hotel Room - Crow Heart": lambda state:
                state.has("has_sword", self.player)
                and RuleUtils.can_passBoxes(self.world, state)
                and state.has("ItemGlove", self.player),
            "Hotel Room - Dog Heart": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player)
                and (bool(self.world.options.obscure)
                     or state.has_any({
                        "ItemSwim",
                        "ItemShoes"
                        }, self.player)
                     or state.has_all({
                            "teleporter switch1",
                            "teleporter switch4",
                            "teleporter switch6",
                            "ItemBasement",
                            }, self.player)),
                # obscure: with good movemnt can do this in 50s
                # -  with just sword glove, adding teleport/swim/shoes
                # - to give more wiggle room outside obscure logic
                # this logic changes if i rando the bone,
                # - don't think i will though

            # Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                state.has("has_sword", self.player)
                and (
                    bool(self.world.options.obscure)
                    or state.has("ItemCoffee", self.player))
                and state.has_all({
                        "ItemBasement",
                        "ItemSwim",
                        }, self.player),
                # obscure: attacking in coyote frames from the right teleporter
                # - lets you do this with just sword/swim

            # Underground Tent
            "Underground Tent - ItemTrophy": lambda state:
                state.has("ItemSwim", self.player),

            # Factory Main
            "Factory Main - ItemMegaSword": lambda state:
                state.has("has_sword", self.player)
                and RuleUtils.has_darkroom(self.world, state, 1)
                and state.has_all({
                    "ItemWateringCan",
                    "left machine",
                    "right machine",
                    "drill smacked",
                    }, self.player),
                # drill shortcut is a vanilla req
            "Factory Main - Cooler Tentacle": lambda state:
                state.has("has_sword", self.player),

            # events
            "generator smashed": lambda state:
                state.has("has_sword", self.player),
            "drill smacked": lambda state:
                state.has("has_sword", self.player),
            "swimmer saved": lambda state:
                True,
            "hostage saved": lambda state:
                state.has("has_sword", self.player),
            "wallet saved": lambda state:
                state.has("has_sword", self.player)
                and state.has_all({
                    "ItemCoffee",
                    "ItemGlove"
                    }, self.player),
            "ninja saved": lambda state:
                state.has("has_sword", self.player) and state.has("ItemGlove", self.player),
            "bridge on": lambda state:
                state.has("has_sword", self.player)
                and (
                     state.has("ItemSwim", self.player)
                     or (
                        RuleUtils.has_darkroom(self.world, state, 2)
                        and state.has("ItemThrow", self.player))
                     or self.factory_to_hotel_backtrack(state)
                ),
            "bridge saved": lambda state:
                state.has("bridge on", self.player),
            "hidden saved": lambda state:
                RuleUtils.can_passBoxes(self.world, state),
            "teleporter switch1": lambda state:
                state.has("has_sword", self.player),
            "teleporter switch4": lambda state:
                state.has("has_sword", self.player)
                and state.has_any({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player),
            "teleporter switch6": lambda state:
                state.has("has_sword", self.player)
                and state.has_any({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player),
            "boatguy watered": lambda state:
                state.has("ItemWateringCan", self.player),
            "left machine": lambda state:
                RuleUtils.has_darkroom(self.world, state, 1)
                and state.has_all({
                    "ItemCoffee",
                    "ItemSwim"
                    }, self.player),
            "right machine": lambda state:
                state.has("has_sword", self.player),
        }

    def factory_to_hotel_backtrack(self, state) -> bool:
        return (state.can_reach("Factory Main", player=self.player)
                and state.has("has_sword", self.player)
                and state.has("ItemPressPass", self.player))

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
