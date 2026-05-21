from typing import TYPE_CHECKING
from rule_builder.rules import And, CanReachRegion, Has, HasAll, HasAny, Or, True_
from . import RuleUtils

if TYPE_CHECKING:
    from . import MinitWorld
else:
    MinitWorld = object

factory_to_hotel_backtrack = HasAll("has_sword", "ItemPressPass") & CanReachRegion("Factory Main")

region_rules = {
    "Menu -> Dog House": True_(),
    "Dog House -> Island Shack": HasAll(
        "has_sword",
        "ItemBoat",
        "boatguy watered",
        "ItemGlove",
        ) | (Or(
            Has("ItemSwim"),
            HasAll(
                "has_sword",
                "ItemBoat",
                "boatguy watered",
                "ItemGlove",
            ),  # TODO: did i not simplify this??
            # you can swim from treasure island by baiting the shark
        ) & RuleUtils.obscure_enabled),
    "Dog House -> Desert RV": Or(
            Has("has_sword") & (
                RuleUtils.has_darkroom2 | Has("ItemGlove")
            ),
            Has("ItemSwim")
        ),
    "Dog House -> Hotel Room": HasAll("has_sword", "ItemGlove") | Has("ItemSwim"),
    "Island Shack -> Basement": HasAll("has_sword", "ItemBasement"),
    "Desert RV -> Factory Main": And(
            Has("has_sword"),
            Has("ItemGrinder") | HasAll("ItemSwim", "ItemCoffee"),
        ),  # swim route needs a damage boost
    "Hotel Room -> Underground Tent": HasAll("has_sword", "ItemGrinder") & RuleUtils.has_darkroom3,
    "Hotel Room -> Factory Main": Or(
            RuleUtils.has_darkroom2 & Has("ItemSwim"),
            And(
                Has("has_sword") | (Has("ItemShoes") & RuleUtils.obscure_enabled),
                # obscure: you can squeeze through the destroyables with shoes and precise movement
                Has("ItemPressPass"),
                HasAny("bombs exploded", "ItemSwim"),
                # swim route needs a damage boost
            ),
        ),
    "Factory Main -> Boss Fight": RuleUtils.has_darkroom2 & RuleUtils.has_megasword,
    "Factory Main -> Hotel Room": factory_to_hotel_backtrack,
}

location_rules = {

    # Dog House
    "Dog House - ItemCoffee": Has("has_sword"),
    "Dog House - ItemFlashLight": Or(
            (Has("ItemSwim") & RuleUtils.obscure_enabled),
            # obscure: you can swim behind the lighthouse and pick up the item
            Has("ItemKey") & HasAny("has_sword", "ItemSwim"),
        ),
    "Dog House - ItemKey": Has("has_sword") & RuleUtils.can_pass_boxes,
    # can swim past the plants, but need to clear the plants by the boxes
    "Dog House - ItemWateringCan": Has("has_sword"),
    "Dog house - ItemBoat": HasAll("has_sword", "ItemGlove"),
    "Dog House - ItemBasement": And(
            HasAll("has_sword", "ItemGlove"),
            Or(
                (Has("ItemSwim") & RuleUtils.obscure_enabled),
                # obscure: you can swim from treasure island by baiting the shark
                HasAll("ItemBoat", "boatguy watered", "ItemGlove"),
            )
        ),
    "Dog House - ItemPressPass": Or(
        RuleUtils.can_pass_boxes & Or(
            HasAll("has_sword", "ItemThrow"),
            Has("ItemSwim"),
            ),
        Has("has_sword") & CanReachRegion("Hotel Room") & HasAll("ItemGrinder", "ItemGlove"),
        (Or(
            HasAll("has_sword", "ItemGrinder", "ItemGlove"),
            # Tile movement from dog house: L U U U R (Glove used at 3 crab and before press house.
            # Grinder used at box going toward press house.)
            RuleUtils.total_hearts(4) & HasAll("ItemSwim", "has_sword"),
            # dog house: L L U R U R U (sword to cut grass to enter toxic river on way to press house)
            RuleUtils.total_hearts(7) & Has("ItemSwim"),
            # Hotel Access is required but implied by having Swim
            ) & RuleUtils.obscure_enabled)
        # obscure: you can, with clean movement and damage tanks,
        # - swim from the factory bridge to press pass house
        # - without any other items
        ),
    "Dog House - House Pot Coin": Has("has_sword"),
    "Dog House - Sewer Island Coin": Has("has_sword") & RuleUtils.has_darkroom3 & RuleUtils.can_open_chest,
    "Dog House - Sewer Coin": HasAll("has_sword", "ItemSwim") & RuleUtils.has_darkroom3 & RuleUtils.can_open_chest,
    "Dog House - Land is Great Coin": RuleUtils.can_open_chest & Or(HasAll("has_sword", "ItemCoffee"), Has("ItemSwim")),
    "Dog House - Hidden Snake Coin":
        HasAny("has_sword", "ItemSwim") & RuleUtils.has_darkroom2 & RuleUtils.can_open_chest,
    "Dog House - Waterfall Coin": RuleUtils.can_open_chest & Has("ItemSwim"),
    "Dog House - Treasure Island Coin": RuleUtils.can_open_chest & Has("ItemSwim"),
    "Dog House - Plant Heart": Has("ItemWateringCan"),
    "Dog House - Bull Heart": Has("has_sword") & Or(CanReachRegion("Desert RV"), RuleUtils.has_darkroom2),
    "Dog House - Boat Tentacle": HasAll("has_sword", "ItemBoat", "boatguy watered", "ItemGlove"),
    "Dog House - Treasure Island Tentacle": HasAll("has_sword", "ItemSwim"),
    "Dog House - Sword Toss Tentacle": HasAll("has_sword", "ItemCoffee", "ItemThrow", "ItemGlove"),
    "Dog House - Sewer Tentacle": HasAll("has_sword", "ItemSwim") & RuleUtils.has_darkroom3,
    "Dog House - Dolphin Heart": Has("ItemWateringCan"),
    # Non Vanilla Location: water the dolphin NPC
    # -  south of the watering can location

    # Desert RV
    "Desert RV - ItemThrow": Has("has_sword"),
    "Desert RV - ItemShoes": Has("Coin", 7),
    "Desert RV - ItemGlove": HasAll("has_sword", "ItemGlove") | HasAny("ItemWateringCan", "ItemSwim"),
    "Desert RV - ItemTurboInk": RuleUtils.has_darkroom2 & Has("Tentacle", 8),
    "Desert RV - Temple Coin": Has("has_sword") & RuleUtils.has_darkroom2 & Or(
        CanReachRegion("Hotel Room") & HasAll("teleporter switch1",
                                              "teleporter switch4",
                                              "teleporter switch6",
                                              "ItemBasement"),
        (Has("ItemSwim") & RuleUtils.obscure_enabled),
        # sword+darkroom+swim should cover the hotel -> temple route
        ),
    # item region implies desert rv access, can teleport implies
    # - island shack access, existing implies dog house access,
    # - only need to check hotel room access
    "Desert RV - Fire Bat Coin": RuleUtils.has_darkroom1 & Has("ItemWateringCan") & RuleUtils.can_open_chest,
    "Desert RV - Truck Supplies Coin": Has("has_sword") & RuleUtils.can_open_chest,
    "Desert RV - Broken Truck": RuleUtils.can_open_chest,
    "Desert RV - Quicksand Coin": Has("has_sword") & RuleUtils.has_darkroom2,
    # vanilla does require sword because the wateringcan drops
    # - while drowing in quicksand
    "Desert RV - Dumpster": Has("has_sword"),
    "Desert RV - Temple Heart": RuleUtils.has_darkroom3 & Has("ItemShoes"),
    "Desert RV - Shop Heart": Has("ItemBasement") & Has("Coin", 19),
    "Desert RV - Octopus Tentacle": Has("has_sword") & RuleUtils.has_darkroom2 & Has("ItemSwim"),
    "Desert RV - Beach Tentacle": Has("has_sword"),
    # redundant rules as swim gets us to the right region anyways
    # or (self.region_DogHouse(state)
    #     and state.has("has_sword", self.player)
    #     and state.has("ItemSwim", self.player)),

    # Hotel Room
    "Hotel Room - ItemSwim": HasAll(
        "swimmer saved",
        "hostage saved",
        "wallet saved",
        "ninja saved",
        "bridge saved",
        "hidden saved",
        ),
    "Hotel Room - ItemGrinder": RuleUtils.has_darkroom2 & HasAll("ItemSwim", "ItemCoffee"),
    "Hotel Room - Shrub Arena Coin": Has("has_sword"),
    "Hotel Room - Miner's Chest Coin":
        Has("has_sword") & RuleUtils.has_darkroom3 & RuleUtils.can_open_chest & Has("ItemGrinder"),
    "Factory Main - Inside Truck": True_(),
    "Hotel Room - Queue": factory_to_hotel_backtrack & HasAny("ItemSwim", "bridge on", "bombs exploded"),
    # swim only uses damage boost
    "Hotel Room - Hotel Backroom Coin": RuleUtils.can_pass_boxes & Has("has_sword"),
    # can be done without sword due to a bug
    "Factory Main - Drill Coin": HasAll("has_sword", "drill smacked"),
    "Hotel Room - Crow Heart": Has("has_sword") & RuleUtils.can_pass_boxes & Has("ItemGlove"),
    "Hotel Room - Dog Heart": HasAll("has_sword", "ItemGlove") & (Or(
        HasAny("ItemSwim", "ItemShoes"),
        HasAll(
            "teleporter switch1",
            "teleporter switch4",
            "teleporter switch6",
            "ItemBasement"),
        ) | RuleUtils.obscure_enabled),
    # obscure: with good movemnt can do this in 50s
    # -  with just sword glove, adding teleport/swim/shoes
    # - to give more wiggle room outside obscure logic
    # this logic changes if i rando the bone,
    # - don't think i will though

    # Island Shack
    "Island Shack - Teleporter Tentacle":
        Has("has_sword") & (Has("ItemCoffee") | RuleUtils.obscure_enabled) & HasAll("ItemBasement", "ItemSwim"),
        # obscure: attacking in coyote frames from the right teleporter
        # - lets you do this with just sword/swim


    # Underground Tent
    "Underground Tent - ItemTrophy": Has("ItemSwim"),

    # Factory Main
    "Factory Main - ItemMegaSword": Has("has_sword") & RuleUtils.has_darkroom1 &
        HasAll(
            "ItemWateringCan",
            "left machine",
            "right machine",
            "generator smashed",
            ),
    "Factory Main - Cooler Tentacle": Has("has_sword"),

    # events
    "generator smashed": Has("has_sword"),
    "drill smacked": HasAll("generator smashed", "has_sword"),
    "swimmer saved": True_(),
    "hostage saved": Has("has_sword"),
    "wallet saved": HasAll("has_sword", "ItemCoffee", "ItemGlove"),
    "ninja saved": HasAll("has_sword", "ItemGlove"),
    "bridge on": Has("has_sword") & Or(
        Has("ItemSwim"),  # damage boost
        Has("bombs exploded"),
        factory_to_hotel_backtrack,
        ),
    "bridge saved": Has("bridge on"),
    "hidden saved": RuleUtils.can_pass_boxes,
    "teleporter switch1": Has("has_sword"),
    "teleporter switch4": Has("has_sword") & HasAny("ItemSwim", "ItemCoffee"),
    "teleporter switch6": Has("has_sword") & HasAny("ItemSwim", "ItemCoffee"),
    "boatguy watered": Has("ItemWateringCan"),
    "left machine": RuleUtils.has_darkroom1 & HasAll("ItemCoffee", "ItemSwim"),
    "right machine": Has("has_sword"),
    "bombs exploded": HasAll("has_sword", "ItemThrow") & RuleUtils.has_darkroom2,
}


class MinitRules:
    world: MinitWorld

    def __init__(self, world: MinitWorld) -> None:
        self.world = world

    def set_Minit_rules(self) -> None:
        for region in self.world.get_regions():
            for entrance in region.entrances:
                if entrance.name in region_rules:
                    self.world.set_rule(entrance, region_rules[entrance.name])
            for location in region.locations:
                if location.name in location_rules:
                    self.world.set_rule(location, location_rules[location.name])
