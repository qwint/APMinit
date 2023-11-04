from BaseClasses import Location, MultiWorld
from typing import NamedTuple, Dict, Optional, Callable


class MinitLocationData(NamedTuple):
    region: str
    code: int = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None
    show_in_spoiler: bool = True


location_table = {

#Dog House
    "Dog House - ItemCoffee": MinitLocationData(
        #logic: Dog House AND sword
        code=60600,
        region="Dog House",),
    "Dog House - ItemFlashLight": MinitLocationData(
        #logic: Dog House AND ItemKey
        code=60601,
        region="Dog House",),
    "Dog House - ItemKey": MinitLocationData(
        #logic: Dog House AND sword AND coffee
        code=60602,
        region="Dog House",),
    "Dog House - ItemWateringCan": MinitLocationData(
        #logic: Dog House AND sword
        code=60603,
        region="Dog House",),
    "Dog house - ItemBoat": MinitLocationData(
        #logic: Dog House AND sword AND glove
        code=60604,
        region="Dog House",),
    "Dog House - ItemBasement": MinitLocationData(
        #logic: Dog House AND sword AND glove AND madeboat(boatwood and watered guy?)
        code=60605,
        region="Dog House",),
    "Dog House - ItemPressPass": MinitLocationData(
        #logic: Dog House AND sword AND coffee AND throw
        #alt logic: Hotel Room AND sword AND grinder AND glove
        #alt logic: Hotel Room AND canTank(lots)
        code=60606,
        region="Dog House",),
    "Dog House - House Pot Coin": MinitLocationData(
        #coin1 - coin
        #logic: Dog House AND sword
        code=60607,
        region="Dog House",),
    "Dog House - Sewer Island Coin": MinitLocationData(
        #coin2 - chest
        #logic: Dog House AND sword AND darkroom
        code=60608,
        region="Dog House",),
    "Dog House - Sewer Coin": MinitLocationData(
        #coin3 - chest
        #logic: Dog House AND sword AND darkroom
        code=60609,
        region="Dog House",),
    "Dog House - Land is Great Coin": MinitLocationData(
        #coin4 - chest
        #logic: Dog House AND sword AND (coffee OR swim)
        code=60610,
        region="Dog House",),
    "Dog House - Hidden Snake Coin": MinitLocationData(
        #coin5 - chest
        #logic: Dog House AND sword AND darkroom
        code=60611,
        region="Dog House",),
    "Dog House - Waterfall Coin": MinitLocationData(
        #coin6 - chest
        #logic: Dog House AND swim
        code=60612,
        region="Dog House",),
    "Dog House - Treasure Island Coin": MinitLocationData(
        #coin7 - chest
        #logic: Dog House AND swim
        code=60613,
        region="Dog House",),
    "Dog House - Plant Heart": MinitLocationData(
        #heartPiece1
        #logic: Dog House AND wateringCan
        code=60614,
        region="Dog House",),
    "Dog House - Bull Heart": MinitLocationData(
        #heartPiece2
        #logic: Dog House AND darkroom() AND sword
        code=60615,
        region="Dog House",),
    "Dog House - Boat Tentacle": MinitLocationData(
        #tentacle1
        #logic: Dog House AND sword AND madeboat()
        code=60616,
        region="Dog House",),
    "Dog House - Treasure Island Tentacle": MinitLocationData(
        #tentacle2
        #logic: Dog House AND sword AND swim
        code=60617,
        region="Dog House",),
    "Dog House - Sword Toss Tentacle": MinitLocationData(
        #tentacle3
        #logic: Dog House AND sword AND coffee AND throw AND glove
        #note, can get past the bridge guards without throw but still need it for the tentacle
        code=60618,
        region="Dog House",),
    "Dog House - Sewer Tentacle": MinitLocationData(
        #tentacle4
        #logic: Dog House AND sword AND darkroom? AND swim
        code=60619,
        region="Dog House",),

#Desert RV
    "Desert RV - ItemThrow": MinitLocationData(
        #logic: Desert RV AND sword
        code=60620,
        region="Desert RV",),
    "Desert RV - ItemShoes": MinitLocationData(
        #logic: Desert RV AND 7 "coin"
        code=60621,
        region="Desert RV",),
    "Desert RV - ItemGlove": MinitLocationData(
        #logic: Desert RV AND wateringCan
        #alt logic: Dog House AND (sword AND glove) OR swim
        code=60622,
        region="Desert RV",),
    "Desert RV - ItemTurboInk": MinitLocationData(
        #logic: Desert RV AND 8 "tentacle"
        code=60623,
        region="Desert RV",),
    "Desert RV - Temple Coin": MinitLocationData(
        #coin8 - chest
        #logic: Desert RV AND ?
        code=60624,
        region="Desert RV",),
    "Desert RV - Fire Bat Coin": MinitLocationData(
        #coin9 - chest
        #logic: Desert RV AND wateringCan
        code=60625,
        region="Desert RV",),
    "Desert RV - Truck Supplies Coin": MinitLocationData(
        #coin10 - chest
        #logic: Desert RV AND sword
        code=60626,
        region="Desert RV",),
    "Desert RV - Broken Truck": MinitLocationData(
        #coin13 - chest
        #logic: Desert RV AND sword
        code=60627,
        region="Desert RV",),
    "Desert RV - Quicksand Coin": MinitLocationData(
        #coin16 - chest
        #logic: Desert RV
        code=60628,
        region="Desert RV",),
    "Desert RV - Dumpster": MinitLocationData(
        #coin19 - coin but you need to hit it
        #logic: Desert RV AND sword
        code=60629,
        region="Desert RV",),
    "Desert RV - Temple Heart": MinitLocationData(
        #heartPiece3
        #logic: Desert RV AND shoes ?(OR grinder)
        code=60630,
        region="Desert RV",),
    "Desert RV - Shop Heart": MinitLocationData(
        #heartPiece4
        #logic: Desert RV AND 19 "coin" ?(AND Basement) 
        code=60631,
        region="Desert RV",),
    "Desert RV - Octopus Tentacle": MinitLocationData(
        #tentacle5
        #logic: Desert RV AND sword AND swim
        code=60632,
        region="Desert RV",),
    "Desert RV - Beach Tentacle": MinitLocationData(
        #tentacle8
        #logic: Desert RV AND sword
        #alt logic: Dog House AND sword AND swim
        code=60633,
        region="Desert RV",),

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
        region="Hotel Room",),
    "Hotel Room - ItemGrinder": MinitLocationData(
        #logic: Hotel Room AND coffee
        code=60635,
        region="Hotel Room",),
    "Hotel Room - Shrub Arena Coin": MinitLocationData(
        #coin11 - coin but you need to stab them
        #logic: Hotel Room AND sword
        code=60636,
        region="Hotel Room",),
    "Hotel Room - Miner's Chest Coin": MinitLocationData(
        #coin12 - chest
        #logic: Hotel Room AND sword AND grinder 
        code=60637,
        region="Hotel Room",),
    "Factory Main - Inside Truck": MinitLocationData(
        #coin14 - coin
        #logic: Hotel Room AND sword AND pressPass AND bridge()
        #alt logic: Desert RV AND grinder
        code=60638,
        region="Factory Main",),
    "Hotel Room - Queue": MinitLocationData(
        #coin15 - coin
        #logic: Hotel Room AND (bridge() OR swim)
        code=60639,
        region="Hotel Room",),
    "Hotel Room - Hotel Backroom Coin": MinitLocationData(
        #coin17 - chest
        #logic: Hotel Room AND coffee AND sword
        code=60640,
        region="Hotel Room",),
    "Factory Main - Drill Coin": MinitLocationData(
        #coin18 - coin
        #logic: Hotel Room AND sword AND bridge() AND pressPass
        code=60641,
        region="Factory Main",),
    "Hotel Room - Crow Heart": MinitLocationData(
        #heartPiece5
        #logic: Hotel Room AND sword AND glove AND coffee
        code=60642,
        region="Hotel Room",),
    "Hotel Room - Dog Heart": MinitLocationData(
        #heartPiece6
        #logic: Hotel Room AND sword AND glove AND basement
        #this logic changes if i rando the bone, don't think i will though
        code=60643,
        region="Hotel Room",),
    "Factory Main - Cooler Tentacle": MinitLocationData(
        #tentacle7
        #logic: Hotel Room AND sword AND pressPass
        #alt logic: through underground and loading dock without pass but likely req shoes
        code=60644,
        region="Factory Main",),

#Island Shack
    "Island Shack - Teleporter Tentacle": MinitLocationData(
        #tentacle6
        #logic: Island Shack AND sword AND basementKey AND (swim OR throw)
        code=60645,
        region="Island Shack",),

#Underground Tent
    "Underground Tent - ItemTrophy": MinitLocationData(
        #logic: Underground Tent
        code=60646,
        region="Underground Tent",),

#Undefined
    # "REGION - ItemCamera": MinitLocationData(
    #     #logic: 
    #     code=60647,
    #     region="Dog House",),

    "Factory Main - ItemMegaSword": MinitLocationData(
        #logic: 
        code=60648,
        region="Factory Main",),
    "Dog House - ItemSword": MinitLocationData(
        #logic: 
        code=60649,
        region="Dog House",),
    "Dog House - Dolphin Heart": MinitLocationData(
        #logic: 
        code=60651,
        region="Dog House",),

    "Fight the Boss": MinitLocationData(
 #       code=60650,
        region="Boss Fight",
 #       locked_item="Boss dead",
        ),

}