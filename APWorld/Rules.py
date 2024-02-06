from BaseClasses import CollectionState
from typing import Dict, Set, Callable, TYPE_CHECKING
from worlds.generic.Rules import set_rule, add_rule
from .Options import MinitGameOptions

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
                (state.has("ItemSwim", self.player)
                    and bool(self.world.options.obscure.value)
                 or (self.has_madeboat(state))),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Dog House -> Desert RV": lambda state:
                state.has("ItemSwim", self.player)
                or (self.has_sword(state) and
                    (state.has("ItemGlove", self.player)
                     or self.has_darkroom(state, 2))),
            "Dog House -> Hotel Room": lambda state:
                state.has("ItemSwim", self.player)
                or (state.has("ItemGlove", self.player)
                    and self.has_sword(state)),
            "Island Shack -> Basement": lambda state:
                state.has("ItemBasement", self.player)
                and self.has_sword(state),
            "Desert RV -> Factory Main": lambda state:
                (state.has("ItemGrinder", self.player)
                    or state.has_all({
                        "ItemSwim",
                        "ItemCoffee"
                        }, self.player))
                and self.has_sword(state),
            "Hotel Room -> Underground Tent": lambda state:
                state.has("ItemGrinder", self.player)
                and self.has_sword(state)
                and self.has_darkroom(state, 3),
            "Hotel Room -> Factory Main": lambda state:
                (state.has("ItemPressPass", self.player)
                    and self.has_sword(state)
                    and (state.has("ItemSwim", self.player)
                         or (self.has_darkroom(state, 3)
                         and state.has("ItemThrow", self.player))))
                or (state.has("ItemSwim", self.player)
                    and self.has_darkroom(state, 2)),
            "Factory Main -> Boss Fight": lambda state:
                self.has_megasword(state)
                and self.has_darkroom(state, 2),
            "Factory Main -> Hotel Room": lambda state:
                self.factory_to_hotel_backtrack(state),
        }

        self.location_rules = {

            # Dog House
            "Dog House - ItemCoffee": lambda state:
                self.has_sword(state),
            "Dog House - ItemFlashLight": lambda state:
                (state.has("ItemKey", self.player)
                    and (state.has("ItemSwim", self.player)
                         or self.has_sword(state)))
                or (state.has("ItemSwim", self.player)
                    and bool(self.world.options.obscure.value)),
                # obscure: you can swim behind the lighthouse
                # - and pick up the item
            "Dog House - ItemKey": lambda state:
                self.has_sword(state) and self.can_passBoxes(state),
                # can swim past the plants,
                # but need to clear the plants by the boxes
            "Dog House - ItemWateringCan": lambda state:
                self.has_sword(state),
            "Dog house - ItemBoat": lambda state:
                state.has("ItemGlove", self.player) and self.has_sword(state),
            "Dog House - ItemBasement": lambda state:
                state.has("ItemGlove", self.player) and self.has_sword(state)
                and ((state.has("ItemSwim", self.player)
                      and bool(self.world.options.obscure.value))
                     or self.has_madeboat(state)),
                # obscure: you can swim from treasure island
                # - by baiting the shark
            "Dog House - ItemPressPass": lambda state:
                ((self.can_passBoxes(state)
                    and ((state.has("ItemThrow", self.player)
                          and self.has_sword(state))
                         or state.has("ItemSwim", self.player)))
                    or (state.can_reach("Hotel Room", player=self.player)
                        and (state.has_all({
                                "ItemGrinder",
                                "ItemGlove"
                                }, self.player)
                             and self.has_sword(state))
                        or (self.total_hearts(state, 4)
                            and state.has("ItemSwim", self.player)
                            and self.has_sword(state))))
                or ((self.total_hearts(state, 7)
                    and bool(self.world.options.obscure.value)
                    and state.can_reach("Hotel Room", player=self.player))
                    and state.has("ItemSwim", self.player)),
                # obscure: you can, with clean movement and damage tanks,
                # - swim from the factory bridge to press pass house
                # - without any other items
            "Dog House - House Pot Coin": lambda state:
                self.has_sword(state),
            "Dog House - Sewer Island Coin": lambda state:
                self.has_sword(state) and self.has_darkroom(state, 3)
                and self.can_openChest(state),
            "Dog House - Sewer Coin": lambda state:
                self.has_sword(state) and self.has_darkroom(state, 3)
                and self.can_openChest(state)
                and state.has("ItemSwim", self.player),
            "Dog House - Land is Great Coin": lambda state:
                self.can_openChest(state)
                and (state.has("ItemSwim", self.player)
                     or (state.has("ItemCoffee", self.player)
                         and self.has_sword(state))),
            "Dog House - Hidden Snake Coin": lambda state:
                (self.has_sword(state) or state.has("ItemSwim", self.player))
                and self.has_darkroom(state, 2) and self.can_openChest(state),
            "Dog House - Waterfall Coin": lambda state:
                state.has("ItemSwim", self.player)
                and self.can_openChest(state),
            "Dog House - Treasure Island Coin": lambda state:
                state.has("ItemSwim", self.player)
                and self.can_openChest(state),
            "Dog House - Plant Heart": lambda state:
                state.has("ItemWateringCan", self.player),
            "Dog House - Bull Heart": lambda state:
                self.has_sword(state)
                and (self.has_darkroom(state, 2)
                     or state.can_reach("Desert RV", player=self.player)),
            "Dog House - Boat Tentacle": lambda state:
                self.has_sword(state) and self.has_madeboat(state),
            "Dog House - Treasure Island Tentacle": lambda state:
                self.has_sword(state) and state.has("ItemSwim", self.player),
            "Dog House - Sword Toss Tentacle": lambda state:
                state.has_all({
                    "ItemCoffee",
                    "ItemThrow",
                    "ItemGlove",
                    }, self.player)
                and self.has_sword(state),
            "Dog House - Sewer Tentacle": lambda state:
                self.has_sword(state) and self.has_darkroom(state, 3)
                and state.has("ItemSwim", self.player),

            # Desert RV
            "Desert RV - ItemThrow": lambda state:
                self.has_sword(state),
            "Desert RV - ItemShoes": lambda state:
                self.get_coins(state, 7),
            "Desert RV - ItemGlove": lambda state:
                state.has("ItemWateringCan", self.player)
                or state.has("ItemSwim", self.player)
                or (self.has_sword(state)
                    and state.has("ItemGlove", self.player)),
            "Desert RV - ItemTurboInk": lambda state:
                self.get_tentacles(state, 8) and self.has_darkroom(state, 2),
            "Desert RV - Temple Coin": lambda state:
                self.has_sword(state) and self.has_darkroom(state, 2)
                and self.can_teleport(state) and state.can_reach("Hotel Room", player=self.player),
                # item region implies desert rv access, can teleport implies
                # - island shack access, existing implies dog house access,
                # - only need to check hotel room access
                # need to revisit logic for obscure swim rules
            "Desert RV - Fire Bat Coin": lambda state:
                state.has("ItemWateringCan", self.player)
                and self.has_darkroom(state, 1) and self.can_openChest(state),
            "Desert RV - Truck Supplies Coin": lambda state:
                self.has_sword(state) and self.can_openChest(state),
            "Desert RV - Broken Truck": lambda state:
                self.can_openChest(state),
            "Desert RV - Quicksand Coin": lambda state:
                self.has_sword(state) and self.has_darkroom(state, 2),
                # vanilla does require sword because the wateringcan drops
                # - while drowing in quicksand
            "Desert RV - Dumpster": lambda state:
                self.has_sword(state),
            "Desert RV - Temple Heart": lambda state:
                state.has("ItemShoes", self.player)
                and self.has_darkroom(state, 3),
            "Desert RV - Shop Heart": lambda state:
                self.get_coins(state, 19)
                and state.has("ItemBasement", self.player),
            "Desert RV - Octopus Tentacle": lambda state:
                self.has_sword(state) and state.has("ItemSwim", self.player)
                and self.has_darkroom(state, 2),
            "Desert RV - Beach Tentacle": lambda state:
                self.has_sword(state),
                # redundant rules as swim gets us to the right region anyways
                # or (self.region_DogHouse(state)
                #     and self.has_sword(state)
                #     and state.has("ItemSwim", self.player)),

            # Hotel Room
            "Hotel Room - ItemSwim": lambda state:
                self.has_savedResidents(state),
            "Hotel Room - ItemGrinder": lambda state:
                state.has_all({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player)
                and self.has_darkroom(state, 2),
            "Hotel Room - Shrub Arena Coin": lambda state:
                self.has_sword(state),
            "Hotel Room - Miner's Chest Coin": lambda state:
                self.has_sword(state) and state.has("ItemGrinder", self.player)
                and self.can_openChest(state) and self.has_darkroom(state, 3),
            "Factory Main - Inside Truck": lambda state: True,
            "Hotel Room - Queue": lambda state:
                state.has_any({"ItemSwim", "bridge on"}, self.player)
                or self.factory_to_hotel_backtrack(state),
            "Hotel Room - Hotel Backroom Coin": lambda state:
                self.can_passBoxes(state) and self.has_sword(state),
            "Factory Main - Drill Coin": lambda state: self.has_sword(state),
            "Hotel Room - Crow Heart": lambda state:
                state.has("ItemGlove", self.player) and self.has_sword(state)
                and self.can_passBoxes(state),
            "Hotel Room - Dog Heart": lambda state:
                (self.has_sword(state) and state.has("ItemGlove", self.player)
                    and (state.has_any({
                            "ItemSwim",
                            "ItemShoes"
                            }, self.player)
                         or self.can_teleport(state)))
                or (self.has_sword(state)
                    and state.has("ItemGlove", self.player)
                    and bool(self.world.options.obscure.value)),
                # obscure: with good movemnt can do this in 50s
                # -  with just sword glove, adding teleport/swim/shoes
                # - to give more wiggle room outside obscure logic
                # this logic changes if i rando the bone,
                # - don't think i will though
            "Factory Main - Cooler Tentacle": lambda state:
                self.has_sword(state),
                # alt logic: through underground and loading dock
                # - without pass but likely req shoes

            # Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                state.has_all({
                        "ItemBasement",
                        "ItemSwim",
                        }, self.player)
                and (state.has("ItemCoffee", self.player)
                     or bool(self.world.options.obscure.value))
                and self.has_sword(state),
                # obscure: attacking in coyote frames from the right teleporter
                # - lets you do this with just sword/swim

            # Underground Tent
            "Underground Tent - ItemTrophy": lambda state:
                state.has("ItemSwim", self.player),
            "Dog House - Dolphin Heart": lambda state:
                state.has("ItemWateringCan", self.player),
                # Non Vanilla Location: water the dolphin NPC
                # -  south of the watering can location

            # Factory Main
            "Factory Main - ItemMegaSword": lambda state:
                state.has_all({
                    "ItemWateringCan",
                    "left machine",
                    "right machine",
                    "drill smacked",
                    }, self.player)
                and self.has_sword(state)
                and self.has_darkroom(state, 1),
                # drill shortcut for swordless entry assumed


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
                state.has_all({
                    "ItemCoffee",
                    "ItemGlove"
                    }, self.player)
                and self.has_sword(state),
            "ninja saved": lambda state:
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "bridge on": lambda state:
                self.has_sword(state)
                and (
                     state.has("ItemSwim", self.player)
                     or (
                        state.has("ItemThrow", self.player)
                        and self.has_sword(state)
                        and self.has_darkroom(state, 2))
                     or (self.factory_to_hotel_backtrack(state))
                ),
            "bridge saved": lambda state:
                state.has("bridge on", self.player),
            "hidden saved": lambda state:
                self.can_passBoxes(state),
            "teleporter switch1": lambda state:
                self.has_sword(state),
            "teleporter switch4": lambda state:
                state.has_any({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player)
                and self.has_sword(state),
            "teleporter switch6": lambda state:
                state.has_any({
                    "ItemSwim",
                    "ItemCoffee"
                    }, self.player)
                and self.has_sword(state),
            "boatguy watered": lambda state:
                state.has("ItemWateringCan", self.player),
            "left machine": lambda state:
                state.has_all({
                    "ItemCoffee",
                    "ItemSwim"
                    }, self.player)
                and self.has_darkroom(state, 1),
            "right machine": lambda state:
                self.has_sword(state),
        }

    def has_sword(self, state) -> bool:
        return state.prog_items[self.player]["has_sword"] > 0

    def has_megasword(self, state) -> bool:
        return (state.has("ItemMegaSword", self.player)
                or (state.count("Progressive Sword", self.player) >= 3)
                or (state.count("Reverse Progressive Sword", self.player) >= 1)
                )

    def has_brokensword(self, state) -> bool:
        return (state.has("ItemBrokenSword", self.player)
                or (state.count("Progressive Sword", self.player) >= 1)
                or (state.count("Reverse Progressive Sword", self.player) >= 3)
                )

    def has_darkroom(self, state, value) -> bool:
        return (state.has("ItemFlashLight", self.player)
                or self.world.options.darkrooms >= value)

    def has_savedResidents(self, state) -> bool:
        # can save all the residents to access the hotel roof
        # - swimmer - true
        # - hostage - sword
        # - wallet - coffee and sword and glove
        # - ninja - sword and glove
        # - bridge - bridge(darkroom? and sword and throw)
        # - hidden - coffee
        # return (self.has_sword(state) and state.has("ItemCoffee", self.player)
        #         and state.has("ItemGlove", self.player)
        #         and (self.has_bridge(state)
        #              or self.factory_to_hotel_backtrack(state)))
        return state.has_all({
            "swimmer saved",
            "hostage saved",
            "wallet saved",
            "ninja saved",
            "bridge saved",
            "hidden saved",
            }, self.player)

    # def has_bridge(self, state) -> bool:
    #     return (state.has("ItemSwim", self.player)
    #             or (self.has_darkroom(state, 2)
    #                 and state.has("ItemThrow", self.player)
    #                 and self.has_sword(state)))
    #     # this is also accessible through the factory
    #     # - in the case that your factory access is desert > sword + grinder
    #     # - and you have press pass, but those are covered by
    #     # - factory_to_hotel_backtrack when necessary

    def has_madeboat(self, state) -> bool:
        return (state.has("ItemBoat", self.player)
                and state.has("boatguy watered", self.player)
                and state.has("ItemGlove", self.player))
        # boatman requires both the watering trigger and having gloves trigger
        # -  to be met before he can spawn, take the boatwood
        # - and repair the boat
    # def has_drillShortcut(self, state) -> bool:
    #     return  self.has_sword(state) and (self.region_factory_hotel(state) or self.region_factory_desert(state))
    #     #allows you to get into the factory with enough time to wait for queue

    def can_openChest(self, state) -> bool:
        return (state.has("ItemWateringCan", self.player)
                or self.has_sword(state))

    def can_passBoxes(self, state) -> bool:
        return (state.has("ItemCoffee", self.player)
                or (self.has_sword(state)
                    and state.has("ItemGrinder", self.player)))

    def can_teleport(self, state) -> bool:
        # return (self.has_madeboat(state)
        #         and state.has("ItemBasement", self.player)
        #         and self.has_sword(state)
        #         and (state.has("ItemSwim", self.player)
        #              or state.has("ItemCoffee", self.player)))
        return (state.has_all({
                "teleporter switch1",
                "teleporter switch4",
                "teleporter switch6",
                }, self.player)
                and state.has("ItemBasement", self.player))

    def get_coins(self, state, count: int) -> bool:
        return state.count("Coin", self.player) >= count

    def get_tentacles(self, state, count: int) -> bool:
        return state.count("Tentacle", self.player) >= count

    def total_hearts(self, state, count: int) -> bool:
        return state.count("HeartPiece", self.player) + 2 >= count

    # def region_DogHouse(self, state) -> bool:
    #     return True

    # def region_DesertRV(self, state) -> bool:
    #     return (self.region_DogHouse(state)
    #             and (self.has_sword(state)
    #                  and state.has("ItemGlove", self.player))
    #             or ((self.has_sword(state)
    #                 or state.has("ItemSwim", self.player))
    #                 and self.has_darkroom(state, 2))
    #             or state.has("ItemSwim", self.player))

    # def region_HotelRoom(self, state) -> bool:
    #     return (self.region_DogHouse(state)
    #             and (self.has_sword(state)
    #                  and state.has("ItemGlove", self.player))
    #             or state.has("ItemSwim", self.player))

    # def region_factory_hotel(self, state) -> bool:
    #     return ((self.has_sword(state)
    #             and state.has("ItemPressPass", self.player)
    #             and ((self.has_darkroom(state, 3)
    #                   and state.has("ItemThrow", self.player))
    #             or state.has("ItemSwim", self.player)))
    #             or (state.has("ItemSwim", self.player)
    #                 and self.has_darkroom(state, 2)))

    # def region_factory_desert(self, state) -> bool:
    #     return ((self.has_sword(state)
    #             and state.has("ItemGrinder", self.player))
    #             or state.has_all({
    #                 "ItemSwim",
    #                 "ItemCoffee"
    #                 }, self.player))

    def factory_to_hotel_backtrack(self, state) -> bool:
        return (state.can_reach("Factory Main", player=self.player)
                and self.has_sword(state)
                and state.has("ItemPressPass", self.player))

    # def region_BossFight(self, state) -> bool:
    #     return (self.has_megasword(state)
    #             and self.has_darkroom(state, 2))

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
