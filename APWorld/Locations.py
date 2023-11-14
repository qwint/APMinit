from BaseClasses import Location, MultiWorld
from typing import NamedTuple, Dict, Optional, Callable


class MinitLocationData(NamedTuple):
    region: str
    code: int = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None
    show_in_spoiler: bool = True


location_table = {

    # Dog House
    "Dog House - ItemCoffee": MinitLocationData(
        code=60600,
        region="Dog House",),
    "Dog House - ItemFlashLight": MinitLocationData(
        code=60601,
        region="Dog House",),
    "Dog House - ItemKey": MinitLocationData(
        code=60602,
        region="Dog House",),
    "Dog House - ItemWateringCan": MinitLocationData(
        code=60603,
        region="Dog House",),
    "Dog house - ItemBoat": MinitLocationData(
        code=60604,
        region="Dog House",),
    "Dog House - ItemBasement": MinitLocationData(
        code=60605,
        region="Dog House",),
    "Dog House - ItemPressPass": MinitLocationData(
        code=60606,
        region="Dog House",),
    "Dog House - House Pot Coin": MinitLocationData(
        # coin1 - coin
        code=60607,
        region="Dog House",),
    "Dog House - Sewer Island Coin": MinitLocationData(
        # coin2 - chest
        code=60608,
        region="Dog House",),
    "Dog House - Sewer Coin": MinitLocationData(
        # coin3 - chest
        code=60609,
        region="Dog House",),
    "Dog House - Land is Great Coin": MinitLocationData(
        # coin4 - chest
        code=60610,
        region="Dog House",),
    "Dog House - Hidden Snake Coin": MinitLocationData(
        # coin5 - chest
        code=60611,
        region="Dog House",),
    "Dog House - Waterfall Coin": MinitLocationData(
        # coin6 - chest
        code=60612,
        region="Dog House",),
    "Dog House - Treasure Island Coin": MinitLocationData(
        # coin7 - chest
        code=60613,
        region="Dog House",),
    "Dog House - Plant Heart": MinitLocationData(
        # heartPiece1
        code=60614,
        region="Dog House",),
    "Dog House - Bull Heart": MinitLocationData(
        # heartPiece2
        code=60615,
        region="Dog House",),
    "Dog House - Boat Tentacle": MinitLocationData(
        # tentacle1
        code=60616,
        region="Dog House",),
    "Dog House - Treasure Island Tentacle": MinitLocationData(
        # tentacle2
        code=60617,
        region="Dog House",),
    "Dog House - Sword Toss Tentacle": MinitLocationData(
        # tentacle3
        code=60618,
        region="Dog House",),
    "Dog House - Sewer Tentacle": MinitLocationData(
        # tentacle4
        code=60619,
        region="Dog House",),

    # Desert RV
    "Desert RV - ItemThrow": MinitLocationData(
        code=60620,
        region="Desert RV",),
    "Desert RV - ItemShoes": MinitLocationData(
        code=60621,
        region="Desert RV",),
    "Desert RV - ItemGlove": MinitLocationData(
        code=60622,
        region="Desert RV",),
    "Desert RV - ItemTurboInk": MinitLocationData(
        code=60623,
        region="Desert RV",),
    "Desert RV - Temple Coin": MinitLocationData(
        # coin8 - chest
        code=60624,
        region="Desert RV",),
    "Desert RV - Fire Bat Coin": MinitLocationData(
        # coin9 - chest
        code=60625,
        region="Desert RV",),
    "Desert RV - Truck Supplies Coin": MinitLocationData(
        # coin10 - chest
        code=60626,
        region="Desert RV",),
    "Desert RV - Broken Truck": MinitLocationData(
        # coin13 - chest
        code=60627,
        region="Desert RV",),
    "Desert RV - Quicksand Coin": MinitLocationData(
        # coin16 - chest
        code=60628,
        region="Desert RV",),
    "Desert RV - Dumpster": MinitLocationData(
        # coin19 - coin but you need to hit it
        code=60629,
        region="Desert RV",),
    "Desert RV - Temple Heart": MinitLocationData(
        # heartPiece3
        code=60630,
        region="Desert RV",),
    "Desert RV - Shop Heart": MinitLocationData(
        # heartPiece4
        code=60631,
        region="Desert RV",),
    "Desert RV - Octopus Tentacle": MinitLocationData(
        # tentacle5
        code=60632,
        region="Desert RV",),
    "Desert RV - Beach Tentacle": MinitLocationData(
        # tentacle8
        code=60633,
        region="Desert RV",),

    # Hotel Room
    "Hotel Room - ItemSwim": MinitLocationData(
        code=60634,
        region="Hotel Room",),
    "Hotel Room - ItemGrinder": MinitLocationData(
        code=60635,
        region="Hotel Room",),
    "Hotel Room - Shrub Arena Coin": MinitLocationData(
        # coin11 - coin but you need to stab them
        code=60636,
        region="Hotel Room",),
    "Hotel Room - Miner's Chest Coin": MinitLocationData(
        # coin12 - chest
        code=60637,
        region="Hotel Room",),
    "Factory Main - Inside Truck": MinitLocationData(
        # coin14 - coin
        code=60638,
        region="Factory Main",),
    "Hotel Room - Queue": MinitLocationData(
        # coin15 - coin
        code=60639,
        region="Hotel Room",),
    "Hotel Room - Hotel Backroom Coin": MinitLocationData(
        # coin17 - chest
        code=60640,
        region="Hotel Room",),
    "Factory Main - Drill Coin": MinitLocationData(
        # coin18 - coin
        code=60641,
        region="Factory Main",),
    "Hotel Room - Crow Heart": MinitLocationData(
        # heartPiece5
        code=60642,
        region="Hotel Room",),
    "Hotel Room - Dog Heart": MinitLocationData(
        # heartPiece6
        code=60643,
        region="Hotel Room",),
    "Factory Main - Cooler Tentacle": MinitLocationData(
        # tentacle7
        code=60644,
        region="Factory Main",),

    # Island Shack
    "Island Shack - Teleporter Tentacle": MinitLocationData(
        # tentacle6
        code=60645,
        region="Island Shack",),

    # Underground Tent
    "Underground Tent - ItemTrophy": MinitLocationData(
        code=60646,
        region="Underground Tent",),

    # Undefined
    # "REGION - ItemCamera": MinitLocationData(
    #     # logic:
    #     code=60647,
    #     region="Dog House",),
    # itemCamera location is replaced by press pass,
    # - will be handled the same in game

    "Factory Main - ItemMegaSword": MinitLocationData(
        code=60648,
        region="Factory Main",),
    "Dog House - ItemSword": MinitLocationData(
        code=60649,
        region="Dog House",),
    "Dog House - Dolphin Heart": MinitLocationData(
        code=60651,
        region="Dog House",),

    "Fight the Boss": MinitLocationData(
        region="Boss Fight",
        # locked_item="Boss dead",
        ),
}
