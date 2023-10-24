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
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - ItemFlashLight": MinitLocationData(
        #logic: Dog House AND ItemKey
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - ItemKey": MinitLocationData(
        #logic: Dog House AND sword AND coffee
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - ItemWateringCan": MinitLocationData(
        #logic: Dog House AND sword
        code=CODENUMBER,
        region="Dog House",),
    "Dog house - ItemBoat": MinitLocationData(
        #logic: Dog House AND sword AND glove
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - ItemBasement": MinitLocationData(
        #logic: Dog House AND sword AND glove AND madeboat(boatwood and watered guy?)
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - itemPressPass": MinitLocationData(
        #logic: Dog House AND sword AND coffee AND throw
        #alt logic: Hotel Room AND sword AND grinder AND glove
        #alt logic: Hotel Room AND canTank(lots)
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - House Pot Coin": MinitLocationData(
        #coin1
        #logic: Dog House AND sword
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Sewer Island Coin": MinitLocationData(
        #coin2
        #logic: Dog House AND sword AND darkroom
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Sewer Coin": MinitLocationData(
        #coin3
        #logic: Dog House AND sword AND darkroom
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Land is Great Coin": MinitLocationData(
        #coin4
        #logic: Dog House AND sword AND (coffee OR swim)
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Hidden Snake Coin": MinitLocationData(
        #coin5
        #logic: Dog House AND sword AND darkroom
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Waterfall Coin": MinitLocationData(
        #coin6
        #logic: Dog House AND swim
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Treasure Island Coin": MinitLocationData(
        #coin7
        #logic: Dog House AND swim
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Plant Heart": MinitLocationData(
        #heartPiece1
        #logic: Dog House AND wateringCan
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Bull Heart": MinitLocationData(
        #heartPiece2
        #logic: Dog House AND darkroom() AND sword
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Boat Tentacle": MinitLocationData(
        #tentacle1
        #logic: Dog House AND sword AND madeboat()
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Treasure Island Tentacle": MinitLocationData(
        #tentacle2
        #logic: Dog House AND sword AND swim
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Sword Toss Tentacle": MinitLocationData(
        #tentacle3
        #logic: Dog House AND sword AND coffee AND throw AND glove
        #note, can get past the bridge guards without throw but still need it for the tentacle
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - Sewer Tentacle": MinitLocationData(
        #tentacle4
        #logic: Dog House AND sword AND darkroom? AND swim
        code=CODENUMBER,
        region="Dog House",),

#Desert RV
    "Desert RV - ItemThrow": MinitLocationData(
        #logic: Desert RV AND sword
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - ItemShoes": MinitLocationData(
        #logic: Desert RV AND 7 "coin"
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - ItemGlove": MinitLocationData(
        #logic: Desert RV AND wateringCan
        #alt logic: Dog House AND (sword AND glove) OR swim
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - ItemTurboInk": MinitLocationData(
        #logic: Desert RV AND 8 "tentacle"
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Temple Coin": MinitLocationData(
        #coin8
        #logic: Desert RV AND ?
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Fire Bat Coin": MinitLocationData(
        #coin9
        #logic: Desert RV AND wateringCan
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Truck Supplies Coin": MinitLocationData(
        #coin10
        #logic: Desert RV AND sword
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Broken Truck": MinitLocationData(
        #coin13
        #logic: Desert RV AND sword
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Quicksand Coin": MinitLocationData(
        #coin16
        #logic: Desert RV
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Dumpster": MinitLocationData(
        #coin19
        #logic: Desert RV AND sword
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Temple Heart": MinitLocationData(
        #heartPiece3
        #logic: Desert RV AND shoes ?(OR grinder)
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Shop Heart": MinitLocationData(
        #heartPiece4
        #logic: Desert RV AND 19 "coin" ?(AND Basement) 
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Octopus Tentacle": MinitLocationData(
        #tentacle5
        #logic: Desert RV AND sword AND swim
        code=CODENUMBER,
        region="Desert RV",),
    "Desert RV - Beach Tentacle": MinitLocationData(
        #tentacle8
        #logic: Desert RV AND sword
        #alt logic: Dog House AND sword AND swim
        code=CODENUMBER,
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
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - ItemGrinder": MinitLocationData(
        #logic: Hotel Room AND coffee
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Shrub Arena Coin": MinitLocationData(
        #coin11
        #logic: Hotel Room AND sword
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Miner's Chest Coin": MinitLocationData(
        #coin12
        #logic: Hotel Room AND sword AND grinder 
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Inside Truck": MinitLocationData(
        #coin14
        #logic: Hotel Room AND sword AND pressPass AND bridge()
        #alt logic: Desert RV AND grinder
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Queue": MinitLocationData(
        #coin15
        #logic: Hotel Room AND (bridge() OR swim)
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Hotel Backroom Coin": MinitLocationData(
        #coin17
        #logic: Hotel Room AND coffee AND sword
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Drill Coin": MinitLocationData(
        #coin18
        #logic: Hotel Room AND sword AND bridge() AND pressPass
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Crow Heart": MinitLocationData(
        #heartPiece5
        #logic: Hotel Room AND sword AND glove AND coffee
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Dog Heart": MinitLocationData(
        #heartPiece6
        #logic: Hotel Room AND sword AND glove AND basement
        #this logic changes if i rando the bone, don't think i will though
        code=CODENUMBER,
        region="Hotel Room",),
    "Hotel Room - Cooler Tentacle": MinitLocationData(
        #tentacle7
        #logic: Hotel Room AND sword AND pressPass
        #alt logic: through underground and loading dock without pass but likely req shoes
        code=CODENUMBER,
        region="Hotel Room",),

#Island Shack
    "Island Shack - Teleporter Tentacle": MinitLocationData(
        #tentacle6
        #logic: Island Shack AND sword AND basementKey AND (swim OR throw)
        code=CODENUMBER,
        region="Island Shack",),

#Underground Tent
    "Underground Tent - ItemTrophy": MinitLocationData(
        #logic: Underground Tent
        code=CODENUMBER,
        region="Underground Tent",),

#Undefined
    "REGION - ItemCamera": MinitLocationData(
        #logic: 
        code=CODENUMBER,
        region="REGION",),

    "REGION - itemMegaSword": MinitLocationData(
        #logic: 
        code=CODENUMBER,
        region="REGION",),
    "REGION - ItemBrokenSword": MinitLocationData(
        #logic: 
        code=CODENUMBER,
        region="REGION",),

    #event locations for spending small and big keys from Pseudoregalia
    # "Dilapidated Dungeon - Unlock Door": MinitLocationData(
    #     region="Dungeon Strong Eyes",
    #     locked_item="Unlocked Door",
    #     show_in_spoiler=False),
    # "Castle Sansa - Unlock Door (Professionalism)": MinitLocationData(
    #     region="Castle Main",
    #     locked_item="Unlocked Door",
    #     show_in_spoiler=False),
    # "Castle Sansa - Unlock Door (Sansa Keep)": MinitLocationData(
    #     region="Castle Main",
    #     locked_item="Unlocked Door",
    #     show_in_spoiler=False),
    # "Sansa Keep - Unlock Door": MinitLocationData(
    #     region="Keep Main",
    #     locked_item="Unlocked Door",
    #     show_in_spoiler=False),
    # "Listless Library - Unlock Door": MinitLocationData(
    #     region="Library Main",
    #     locked_item="Unlocked Door",
    #     show_in_spoiler=False),
    # "Twilight Theatre - Unlock Door": MinitLocationData(
    #     region="Theatre Main",
    #     locked_item="Unlocked Door",
    #     show_in_spoiler=False),
    # "The Underbelly - Unlock Door": MinitLocationData(
    #     region="Underbelly Main",
    #     locked_item="Unlocked Door",
    #     show_in_spoiler=False),

    # "D S T RT ED M M O   Y": MinitLocationData(
    #     region="The Great Door",
    #     locked_item="Something Worth Being Awake For"),
}