from BaseClasses import Location, MultiWorld
from typing import NamedTuple, Dict, Optional, Callable


class MinitLocationData(NamedTuple):
    region: str
    er_region: str
    code: int = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None
    show_in_spoiler: bool = True


location_table = {

    # Dog House
    "Dog House - ItemCoffee": MinitLocationData(
        code=60600,
        region="Dog House",
        er_region="coffee shop inside",),
    "Dog House - ItemFlashLight": MinitLocationData(
        code=60601,
        region="Dog House",
        er_region="lighthouse lookout",),
    "Dog House - ItemKey": MinitLocationData(
        code=60602,
        region="Dog House",
        er_region="key room",),
    "Dog House - ItemWateringCan": MinitLocationData(
        code=60603,
        region="Dog House",
        er_region="watering can",),
    "Dog house - ItemBoat": MinitLocationData(
        code=60604,
        region="Dog House",
        er_region="boattree main",),
    "Dog House - ItemBasement": MinitLocationData(
        code=60605,
        region="Dog House",
        er_region="Overworld",),
    "Dog House - ItemPressPass": MinitLocationData(
        code=60606,
        region="Dog House",
        er_region="camera house inside",),
    "Dog House - House Pot Coin": MinitLocationData(
        # coin1 - coin
        code=60607,
        region="Dog House",
        er_region="dog house inside",),
    "Dog House - Sewer Island Coin": MinitLocationData(
        # coin2 - chest
        code=60608,
        region="Dog House",
        er_region="sewer island",),
    "Dog House - Sewer Coin": MinitLocationData(
        # coin3 - chest
        code=60609,
        region="Dog House",
        er_region="sewer upper",),
    "Dog House - Land is Great Coin": MinitLocationData(
        # coin4 - chest
        code=60610,
        region="Dog House",
        er_region="above lighthouse land",),
    "Dog House - Hidden Snake Coin": MinitLocationData(
        # coin5 - chest
        code=60611,
        region="Dog House",
        er_region="snake west",),
    "Dog House - Waterfall Coin": MinitLocationData(
        # coin6 - chest
        code=60612,
        region="Dog House",
        er_region="waterfall cave",),
    "Dog House - Treasure Island Coin": MinitLocationData(
        # coin7 - chest
        code=60613,
        region="Dog House",
        er_region="Overworld",),
    "Dog House - Plant Heart": MinitLocationData(
        # heartPiece1
        code=60614,
        region="Dog House",
        er_region="plant main",),
    "Dog House - Bull Heart": MinitLocationData(
        # heartPiece2
        code=60615,
        region="Dog House",
        er_region="bull room",),
    "Dog House - Boat Tentacle": MinitLocationData(
        # tentacle1
        code=60616,
        region="Dog House",
        er_region="boat land",),
    "Dog House - Treasure Island Tentacle": MinitLocationData(
        # tentacle2
        code=60617,
        region="Dog House",
        er_region="Overworld",),
    "Dog House - Sword Toss Tentacle": MinitLocationData(
        # tentacle3
        code=60618,
        region="Dog House",
        er_region="throwcheck box",),
    "Dog House - Sewer Tentacle": MinitLocationData(
        # tentacle4
        code=60619,
        region="Dog House",
        er_region="sewer tentacle",),

    # Desert RV
    "Desert RV - ItemThrow": MinitLocationData(
        code=60620,
        region="Desert RV",
        er_region="Overworld",),
    "Desert RV - ItemShoes": MinitLocationData(
        code=60621,
        region="Desert RV",
        er_region="shoe shop inside",),
    "Desert RV - ItemGlove": MinitLocationData(
        code=60622,
        region="Desert RV",
        er_region="glove inside",),
    "Desert RV - ItemTurboInk": MinitLocationData(
        code=60623,
        region="Desert RV",
        er_region="temple octopus",),
    "Desert RV - Temple Coin": MinitLocationData(
        # coin8 - chest
        code=60624,
        region="Desert RV",
        er_region="temple coin chest",),
    "Desert RV - Fire Bat Coin": MinitLocationData(
        # coin9 - chest
        code=60625,
        region="Desert RV",
        er_region="temple firebat chest",),
    "Desert RV - Truck Supplies Coin": MinitLocationData(
        # coin10 - chest
        code=60626,
        region="Desert RV",
        er_region="factory loading lower shortcut",),
    "Desert RV - Broken Truck": MinitLocationData(
        # coin13 - chest
        code=60627,
        region="Desert RV",
        er_region="Overworld",),
    "Desert RV - Quicksand Coin": MinitLocationData(
        # coin16 - chest
        code=60628,
        region="Desert RV",
        er_region="quicksand main",),
    "Desert RV - Dumpster": MinitLocationData(
        # coin19 - coin but you need to hit it
        code=60629,
        region="Desert RV",
        er_region="shoe shop outside",),
    "Desert RV - Temple Heart": MinitLocationData(
        # heartPiece3
        code=60630,
        region="Desert RV",
        er_region="temple heart",),
    "Desert RV - Shop Heart": MinitLocationData(
        # heartPiece4
        code=60631,
        region="Desert RV",
        er_region="shoe shop downstairs",),
    "Desert RV - Octopus Tentacle": MinitLocationData(
        # tentacle5
        code=60632,
        region="Desert RV",
        er_region="temple tentacle",),
    "Desert RV - Beach Tentacle": MinitLocationData(
        # tentacle8
        code=60633,
        region="Desert RV",
        er_region="desert beach land",),

    # Hotel Room
    "Hotel Room - ItemSwim": MinitLocationData(
        code=60634,
        region="Hotel Room",
        er_region="hotel outside",),
    "Hotel Room - ItemGrinder": MinitLocationData(
        code=60635,
        region="Hotel Room",
        er_region="grinder main",),
    "Hotel Room - Shrub Arena Coin": MinitLocationData(
        # coin11 - coin but you need to stab them
        code=60636,
        region="Hotel Room",
        er_region="arena main",),
    "Hotel Room - Miner's Chest Coin": MinitLocationData(
        # coin12 - chest
        code=60637,
        region="Hotel Room",
        er_region="miner chest belts",),
    "Factory Main - Inside Truck": MinitLocationData(
        # coin14 - coin
        code=60638,
        region="Factory Main",
        er_region="factory loading upper",),
    "Hotel Room - Queue": MinitLocationData(
        # coin15 - coin
        code=60639,
        region="Hotel Room",
        er_region="factory queue",),
    "Hotel Room - Hotel Backroom Coin": MinitLocationData(
        # coin17 - chest
        code=60640,
        region="Hotel Room",
        er_region="hotel backroom",),
    "Factory Main - Drill Coin": MinitLocationData(
        # coin18 - coin
        code=60641,
        region="Factory Main",
        er_region="factory drill",),
    "Hotel Room - Crow Heart": MinitLocationData(
        # heartPiece5
        code=60642,
        region="Hotel Room",
        er_region="crowroom",),
    "Hotel Room - Dog Heart": MinitLocationData(
        # heartPiece6
        code=60643,
        region="Hotel Room",
        er_region="dog house inside",),
    "Factory Main - Cooler Tentacle": MinitLocationData(
        # tentacle7
        code=60644,
        region="Factory Main",
        er_region="factory cooler east",),

    # Island Shack
    "Island Shack - Teleporter Tentacle": MinitLocationData(
        # tentacle6
        code=60645,
        region="Island Shack",
        er_region="teleporter tentacle",),

    # Underground Tent
    "Underground Tent - ItemTrophy": MinitLocationData(
        code=60646,
        region="Underground Tent",
        er_region="trophy room",),

    # Undefined
    # "REGION - ItemCamera": MinitLocationData(
    #     # logic:
    #     code=60647,
    #     region="Dog House",
    #    er_region="camera house inside",),
    # itemCamera location is replaced by press pass,
    # - will be handled the same in game
    # itemCamera location is replaced by press pass,
    # - will be handled the same in game
    # itemCamera location is replaced by press pass, will be handled the same in game

    "Factory Main - ItemMegaSword": MinitLocationData(
        code=60648,
        region="Factory Main",
        er_region="megasword lower",),
    "Dog House - ItemSword": MinitLocationData(
        code=60649,
        region="Dog House",
        er_region="sword main",),
    "Dog House - Dolphin Heart": MinitLocationData(
        code=60651,
        region="Dog House",
        er_region="dolphin land",),

    "Fight the Boss": MinitLocationData(
        region="Boss Fight",
        er_region="factory machine generator",
        locked_item="Boss dead",
        ),
    "Flush the Sword": MinitLocationData(
        region="Factory Main",
        er_region="factory toilet",
        locked_item="Sword Flushed",
        ),
    "generator smashed": MinitLocationData(
        region="Factory Main",
        er_region="factory machine generator",
        locked_item="generator smashed",
        ),
    "drill smacked": MinitLocationData(
        region="Factory Main",
        er_region="factory drill",
        locked_item="drill smacked",
        ),
    "swimmer saved": MinitLocationData(
        region="Hotel Room",
        er_region="diver room",
        locked_item="swimmer saved",
        ),
    "hostage saved": MinitLocationData(
        region="Hotel Room",
        er_region="arena main",
        locked_item="hostage saved",
        ),
    "wallet saved": MinitLocationData(
        region="Hotel Room",
        er_region="wallet room",
        locked_item="wallet saved",
        ),
    "ninja saved": MinitLocationData(
        region="Hotel Room",
        er_region="tree resident",
        locked_item="ninja saved",
        ),
    "bridge on": MinitLocationData(
        region="Hotel Room",
        er_region="bridge switch right",
        locked_item="bridge on",
        ),
    "bridge saved": MinitLocationData(
        region="Hotel Room",
        er_region="bridge right",
        locked_item="bridge saved",
        ),
    "hidden saved": MinitLocationData(
        region="Hotel Room",
        er_region="bridge switch left",
        locked_item="hidden saved",
        ),
    "teleporter switch1": MinitLocationData(
        region="Island Shack",
        er_region="teleporter switch1",
        locked_item="teleporter switch1",
        ),
    "teleporter switch4": MinitLocationData(
        region="Island Shack",
        er_region="Overworld",
        locked_item="teleporter switch4",
        ),
    "teleporter switch6": MinitLocationData(
        region="Island Shack",
        er_region="Overworld",
        locked_item="teleporter switch6",
        ),
    "boatguy watered": MinitLocationData(
        region="Desert RV",
        er_region="Overworld",
        locked_item="boatguy watered",
        ),
    "left machine": MinitLocationData(
        region="Factory Main",
        er_region="grinder main",
        locked_item="left machine",
        ),
    "right machine": MinitLocationData(
        region="Factory Main",
        er_region="factory switch test",
        locked_item="right machine",
        ),
}
