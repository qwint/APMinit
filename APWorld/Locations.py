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

#Dog House
    "Dog House - ItemCoffee": MinitLocationData(
        #logic: Dog House AND sword
        code=60600,
        region="Dog House",
        er_region="coffee shop inside",),
    "Dog House - ItemFlashLight": MinitLocationData(
        #logic: Dog House AND ItemKey
        code=60601,
        region="Dog House",
        er_region="lighthouse lookout",),
    "Dog House - ItemKey": MinitLocationData(
        #logic: Dog House AND sword AND coffee
        code=60602,
        region="Dog House",
        er_region="key room",),
    "Dog House - ItemWateringCan": MinitLocationData(
        #logic: Dog House AND sword
        code=60603,
        region="Dog House",
        er_region="watering can",),
    "Dog house - ItemBoat": MinitLocationData(
        #logic: Dog House AND sword AND glove
        code=60604,
        region="Dog House",
        er_region="boattree main",),
    "Dog House - ItemBasement": MinitLocationData(
        #logic: Dog House AND sword AND glove AND madeboat(boatwood and watered guy?)
        code=60605,
        region="Dog House",
        er_region="Overworld",),
    "Dog House - ItemPressPass": MinitLocationData(
        #logic: Dog House AND sword AND coffee AND throw
        #alt logic: Hotel Room AND sword AND grinder AND glove
        #alt logic: Hotel Room AND canTank(lots)
        code=60606,
        region="Dog House",
        er_region="camera house inside",),
    "Dog House - House Pot Coin": MinitLocationData(
        #coin1 - coin
        #logic: Dog House AND sword
        code=60607,
        region="Dog House",
        er_region="dog house inside",),
    "Dog House - Sewer Island Coin": MinitLocationData(
        #coin2 - chest
        #logic: Dog House AND sword AND darkroom
        code=60608,
        region="Dog House",
        er_region="sewer island",),
    "Dog House - Sewer Coin": MinitLocationData(
        #coin3 - chest
        #logic: Dog House AND sword AND darkroom
        code=60609,
        region="Dog House",
        er_region="sewer upper",),
    "Dog House - Land is Great Coin": MinitLocationData(
        #coin4 - chest
        #logic: Dog House AND sword AND (coffee OR swim)
        code=60610,
        region="Dog House",
        er_region="above lighthouse land",),
    "Dog House - Hidden Snake Coin": MinitLocationData(
        #coin5 - chest
        #logic: Dog House AND sword AND darkroom
        code=60611,
        region="Dog House",
        er_region="snake west",),
    "Dog House - Waterfall Coin": MinitLocationData(
        #coin6 - chest
        #logic: Dog House AND swim
        code=60612,
        region="Dog House",
        er_region="waterfall cave",),
    "Dog House - Treasure Island Coin": MinitLocationData(
        #coin7 - chest
        #logic: Dog House AND swim
        code=60613,
        region="Dog House",
        er_region="Overworld",),
    "Dog House - Plant Heart": MinitLocationData(
        #heartPiece1
        #logic: Dog House AND wateringCan
        code=60614,
        region="Dog House",
        er_region="plant main",),
    "Dog House - Bull Heart": MinitLocationData(
        #heartPiece2
        #logic: Dog House AND darkroom() AND sword
        code=60615,
        region="Dog House",
        er_region="bull room",),
    "Dog House - Boat Tentacle": MinitLocationData(
        #tentacle1
        #logic: Dog House AND sword AND madeboat()
        code=60616,
        region="Dog House",
        er_region="boat land",),
    "Dog House - Treasure Island Tentacle": MinitLocationData(
        #tentacle2
        #logic: Dog House AND sword AND swim
        code=60617,
        region="Dog House",
        er_region="Overworld",),
    "Dog House - Sword Toss Tentacle": MinitLocationData(
        #tentacle3
        #logic: Dog House AND sword AND coffee AND throw AND glove
        #note, can get past the bridge guards without throw but still need it for the tentacle
        code=60618,
        region="Dog House",
        er_region="throwcheck box",),
    "Dog House - Sewer Tentacle": MinitLocationData(
        #tentacle4
        #logic: Dog House AND sword AND darkroom? AND swim
        code=60619,
        region="Dog House",
        er_region="sewer tentacle",),

#Desert RV
    "Desert RV - ItemThrow": MinitLocationData(
        #logic: Desert RV AND sword
        code=60620,
        region="Desert RV",
        er_region="Overworld",),
    "Desert RV - ItemShoes": MinitLocationData(
        #logic: Desert RV AND 7 "coin"
        code=60621,
        region="Desert RV",
        er_region="shoe shop inside",),
    "Desert RV - ItemGlove": MinitLocationData(
        #logic: Desert RV AND wateringCan
        #alt logic: Dog House AND (sword AND glove) OR swim
        code=60622,
        region="Desert RV",
        er_region="glove inside",),
    "Desert RV - ItemTurboInk": MinitLocationData(
        #logic: Desert RV AND 8 "tentacle"
        code=60623,
        region="Desert RV",
        er_region="temple octopus",),
    "Desert RV - Temple Coin": MinitLocationData(
        #coin8 - chest
        #logic: Desert RV AND ?
        code=60624,
        region="Desert RV",
        er_region="temple coin chest",),
    "Desert RV - Fire Bat Coin": MinitLocationData(
        #coin9 - chest
        #logic: Desert RV AND wateringCan
        code=60625,
        region="Desert RV",
        er_region="temple firebat chest",),
    "Desert RV - Truck Supplies Coin": MinitLocationData(
        #coin10 - chest
        #logic: Desert RV AND sword
        code=60626,
        region="Desert RV",
        er_region="factory loading lower shortcut",),
    "Desert RV - Broken Truck": MinitLocationData(
        #coin13 - chest
        #logic: Desert RV AND sword
        code=60627,
        region="Desert RV",
        er_region="Overworld",),
    "Desert RV - Quicksand Coin": MinitLocationData(
        #coin16 - chest
        #logic: Desert RV
        code=60628,
        region="Desert RV",
        er_region="quicksand main",),
    "Desert RV - Dumpster": MinitLocationData(
        #coin19 - coin but you need to hit it
        #logic: Desert RV AND sword
        code=60629,
        region="Desert RV",
        er_region="shoe shop outside",),
    "Desert RV - Temple Heart": MinitLocationData(
        #heartPiece3
        #logic: Desert RV AND shoes ?(OR grinder)
        code=60630,
        region="Desert RV",
        er_region="temple heart",),
    "Desert RV - Shop Heart": MinitLocationData(
        #heartPiece4
        #logic: Desert RV AND 19 "coin" ?(AND Basement) 
        code=60631,
        region="Desert RV",
        er_region="shoe shop downstairs",),
    "Desert RV - Octopus Tentacle": MinitLocationData(
        #tentacle5
        #logic: Desert RV AND sword AND swim
        code=60632,
        region="Desert RV",
        er_region="temple tentacle",),
    "Desert RV - Beach Tentacle": MinitLocationData(
        #tentacle8
        #logic: Desert RV AND sword
        #alt logic: Dog House AND sword AND swim
        code=60633,
        region="Desert RV",
        er_region="desert beach land",),

#Hotel Room
    "Hotel Room - ItemSwim": MinitLocationData(
        #logic: Hotel Room AND savedResidents(
        #swimmer - true
        #hostage - sword
        #wallet - coffee AND sword AND glove
        #ninja - sword AND glove
        #bridge - bridge(darkroom? AND sword AND throw)
        #hidden - coffee
        code=60634,
        region="Hotel Room",
        er_region="hotel outside",),
    "Hotel Room - ItemGrinder": MinitLocationData(
        #logic: Hotel Room AND coffee
        code=60635,
        region="Hotel Room",
        er_region="grinder main",),
    "Hotel Room - Shrub Arena Coin": MinitLocationData(
        #coin11 - coin but you need to stab them
        #logic: Hotel Room AND sword
        code=60636,
        region="Hotel Room",
        er_region="arena main",),
    "Hotel Room - Miner's Chest Coin": MinitLocationData(
        #coin12 - chest
        #logic: Hotel Room AND sword AND grinder 
        code=60637,
        region="Hotel Room",
        er_region="miner chest belts",),
    "Factory Main - Inside Truck": MinitLocationData(
        #coin14 - coin
        #logic: Hotel Room AND sword AND pressPass AND bridge()
        #alt logic: Desert RV AND grinder
        code=60638,
        region="Factory Main",
        er_region="factory loading upper",),
    "Hotel Room - Queue": MinitLocationData(
        #coin15 - coin
        #logic: Hotel Room AND (bridge() OR swim)
        code=60639,
        region="Hotel Room",
        er_region="factory queue",),
    "Hotel Room - Hotel Backroom Coin": MinitLocationData(
        #coin17 - chest
        #logic: Hotel Room AND coffee AND sword
        code=60640,
        region="Hotel Room",
        er_region="hotel backroom",),
    "Factory Main - Drill Coin": MinitLocationData(
        #coin18 - coin
        #logic: Hotel Room AND sword AND bridge() AND pressPass
        code=60641,
        region="Factory Main",
        er_region="factory drill",),
    "Hotel Room - Crow Heart": MinitLocationData(
        #heartPiece5
        #logic: Hotel Room AND sword AND glove AND coffee
        code=60642,
        region="Hotel Room",
        er_region="crowroom",),
    "Hotel Room - Dog Heart": MinitLocationData(
        #heartPiece6
        #logic: Hotel Room AND sword AND glove AND basement
        #this logic changes if i rando the bone, don't think i will though
        code=60643,
        region="Hotel Room",
        er_region="dog house inside",),
    "Factory Main - Cooler Tentacle": MinitLocationData(
        #tentacle7
        #logic: Hotel Room AND sword AND pressPass
        #alt logic: through underground and loading dock without pass but likely req shoes
        code=60644,
        region="Factory Main",
        er_region="factory cooler east",),

#Island Shack
    "Island Shack - Teleporter Tentacle": MinitLocationData(
        #tentacle6
        #logic: Island Shack AND sword AND basementKey AND (swim OR throw)
        code=60645,
        region="Island Shack",
        er_region="teleporter tentacle",),

#Underground Tent
    "Underground Tent - ItemTrophy": MinitLocationData(
        #logic: Underground Tent
        code=60646,
        region="Underground Tent",
        er_region="trophy room",),

#Undefined
    # "REGION - ItemCamera": MinitLocationData(
    #     #logic: 
    #     code=60647,
    #     region="Dog House",
    #    er_region="camera house inside",),

    "Factory Main - ItemMegaSword": MinitLocationData(
        #logic: 
        code=60648,
        region="Factory Main",
        er_region="megasword lower",),
    "Dog House - ItemSword": MinitLocationData(
        #logic: 
        code=60649,
        region="Dog House",
        er_region="sword main",),
    "Dog House - Dolphin Heart": MinitLocationData(
        #logic: 
        code=60651,
        region="Dog House",
        er_region="dolphin land",),

    "Fight the Boss": MinitLocationData(
 #       code=60650,
        region="Boss Fight",
        er_region="factory machine generator"
 #       locked_item="Boss dead",
        ),

}