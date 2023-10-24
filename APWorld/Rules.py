from BaseClasses import CollectionState
from typing import Dict, Set, Callable, TYPE_CHECKING
from worlds.generic.Rules import set_rule

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
            "Menu -> Dog House": lambda state: True,
            "Dog House -> Island Shack": lambda state: 
                has_madeboat(state),
            "Dog House -> Desert RV": lambda state:
                has_sword(state) and state.has("ItemGlove", self.player)
                or has_sword(state) and has_darkroom(state)
                or state.has("ItemSwim", self.player),
            "Dog House -> Hotel Room": lambda state: 
                has_sword(state) and state.has("ItemGlove", self.player),
            "Island Shack -> Basement": lambda state:
                has_sword(state) and state.has("ItemBasement", self.player),
            #"Desert RV -> Dog House": lambda state: True,
            #"Hotel Room -> Dog House": lambda state: True,
            #"Underground Tent -> Dog House": lambda state: True,
            #have no idea how to do this btw
            "Basement -> Dog House": lambda state: True,
            "Basement -> Island Shack": lambda state: True,
            "Basement -> Hotel Room": lambda state: True,
            "Hotel Room -> Underground Tent": lambda state: 
                has_sword(state) and has_darkroom(state) and state.has("ItemGrinder", self.player),
           "Hotel Room -> Boss Fight": lambda state: 
                state.has("ItemPressPass", self.player) and self.has_bridge(state)
        }

        self.location_rules = {
        #TODO: implement alt logic

        #Dog House
            "Dog House - ItemCoffee": lambda state:
                #logic: Dog House and sword
                self.has_sword(state),
            "Dog House - ItemFlashLight": lambda state:
                #logic: Dog House and ItemKey
                state.has("ItemKey", self.player),
            "Dog House - ItemKey": lambda state:
                #logic: Dog House and sword and coffee
                self.has_sword(state) and state.has("ItemCoffee", self.player),
            "Dog House - ItemWateringCan": lambda state:
                #logic: Dog House and sword
                self.has_sword(state),
            "Dog house - ItemBoat": lambda state:
                #logic: Dog House and sword and glove
                self.has_sword(state) and state.has("ItemGlove", self.player),
            "Dog House - ItemBasement": lambda state:
                #logic: Dog House and sword and glove and madeboat(boatwood and watered guy?)
                self.has_sword(state) and state.has("ItemGlove", self.player) and self.has_madeboat(state),
            "Dog House - ItemPressPass": lambda state:
                #logic: Dog House and sword and coffee and throw
                self.has_sword(state) and state.has("ItemCoffee", self.player) and state.has("ItemThrow", self.player),
                #alt logic: Hotel Room and sword and grinder and glove
                #alt logic: Hotel Room and canTank(lots)
            "Dog House - House Pot Coin": lambda state:
                #coin1
                #logic: Dog House and sword
                self.has_sword(state),
            "Dog House - Sewer Island Coin": lambda state:
                #coin2
                #logic: Dog House and sword and darkroom
                self.has_sword(state) and self.has_darkroom(state),
            "Dog House - Sewer Coin": lambda state:
                #coin3
                #logic: Dog House and sword and darkroom
                self.has_sword(state) and self.has_darkroom(state),
            "Dog House - Land is Great Coin": lambda state:
                #coin4
                #logic: Dog House and sword and (coffee or swim)
                self.has_sword(state) and (state.has("ItemCoffee", self.player) 
                or state.has("ItemSwim", self.player)),
            "Dog House - Hidden Snake Coin": lambda state:
                #coin5
                #logic: Dog House and sword and darkroom
                self.has_sword(state) and self.has_darkroom(state),
            "Dog House - Waterfall Coin": lambda state:
                #coin6
                #logic: Dog House and swim
                state.has("ItemSwim", self.player),
            "Dog House - Treasure Island Coin": lambda state:
                #coin7
                #logic: Dog House and swim
                state.has("ItemSwim", self.player),
            "Dog House - Plant Heart": lambda state:
                #heartPiece1
                #logic: Dog House and wateringCan
                state.has("ItemWateringCan", self.player),
            "Dog House - Bull Heart": lambda state:
                #heartPiece2
                #logic: Dog House and darkroom() and sword
                self.has_darkroom(state)() and self.has_sword(state),
            "Dog House - Boat Tentacle": lambda state:
                #tentacle1
                #logic: Dog House and sword and madeboat()
                self.has_sword(state) and self.has_madeboat(state),
            "Dog House - Treasure Island Tentacle": lambda state:
                #tentacle2
                #logic: Dog House and sword and swim
                self.has_sword(state) and state.has("ItemSwim", self.player),
            "Dog House - Sword Toss Tentacle": lambda state:
                #tentacle3
                #logic: Dog House and sword and coffee and throw and glove
                self.has_sword(state) and state.has("ItemCoffee", self.player) and state.has("ItemThrow", self.player) and state.has("ItemGlove", self.player),
                #note, can get past the bridge guards without throw but still need it for the tentacle
            "Dog House - Sewer Tentacle": lambda state:
                #tentacle4
                #logic: Dog House and sword and darkroom? and swim
                self.has_sword(state) and self.has_darkroom(state) and state.has("ItemSwim", self.player),

        #Desert RV
            "Desert RV - ItemThrow": lambda state:
                #logic: Desert RV and sword
                self.has_sword(state),
            "Desert RV - ItemShoes": lambda state:
                #logic: Desert RV and 7 "coin"
                self.get_coins(state, 7),
            "Desert RV - ItemGlove": lambda state:
                #logic: Desert RV and wateringCan
                state.has("ItemWateringCan", self.player),
                #alt logic: Dog House and (sword and glove) or swim
            "Desert RV - ItemTurboInk": lambda state:
                #logic: Desert RV and 8 "tentacle"
                self.get_tentacles(state, 8),
            "Desert RV - Temple Coin": lambda state: True,
                #coin8
                #logic: Desert RV and ?
            "Desert RV - Fire Bat Coin": lambda state:
                #coin9
                #logic: Desert RV and wateringCan
                state.has("ItemWateringCan", self.player),
            "Desert RV - Truck Supplies Coin": lambda state:
                #coin10
                #logic: Desert RV and sword
                self.has_sword(state),
            "Desert RV - Broken Truck": lambda state:
                #coin13
                #logic: Desert RV and sword
                self.has_sword(state),
            "Desert RV - Quicksand Coin": lambda state: True,
                #coin16
                #logic: Desert RV
            "Desert RV - Dumpster": lambda state:
                #coin19
                #logic: Desert RV and sword
                self.has_sword(state),
            "Desert RV - Temple Heart": lambda state:
                #heartPiece3
                #logic: Desert RV and shoes ?(or grinder)
                state.has("ItemShoes", self.player) or state.has("ItemGrinder", self.player),
            "Desert RV - Shop Heart": lambda state:
                #heartPiece4
                #logic: Desert RV and 19 "coin" ?(and Basement) 
                self.get_coins(state, 19) and Basement ,
            "Desert RV - Octopus Tentacle": lambda state:
                #tentacle5
                #logic: Desert RV and sword and swim
                self.has_sword(state) and state.has("ItemSwim", self.player),
            "Desert RV - Beach Tentacle": lambda state:
                #tentacle8
                #logic: Desert RV and sword
                self.has_sword(state),
                #alt logic: Dog House and sword and swim

        #Hotel Room
            "Hotel Room - ItemSwim": lambda state:
                #logic: Hotel Room and savedResidents(
                self.has_savedResidents(state),
                #swimmer - true
                #hostage - sword
                #wallet - coffee and sword and glove
                #ninja - sword and glove
                #bridge - bridge(darkroom? and sword and throw)
                #hidden - coffee
            "Hotel Room - ItemGrinder": lambda state:
                #logic: Hotel Room and coffee
                state.has("ItemCoffee", self.player),
            "Hotel Room - Shrub Arena Coin": lambda state:
                #coin11
                #logic: Hotel Room and sword
                self.has_sword(state),
            "Hotel Room - Miner's Chest Coin": lambda state:
                #coin12
                #logic: Hotel Room and sword and grinder 
                self.has_sword(state) and state.has("ItemGrinder", self.player) ,
            "Hotel Room - Inside Truck": lambda state:
                #coin14
                #logic: Hotel Room and sword and pressPass and bridge()
                self.has_sword(state) and state.has("ItemPressPass", self.player) and self.has_bridge(state),
                #alt logic: Desert RV and grinder
            "Hotel Room - Queue": lambda state:
                #coin15
                #logic: Hotel Room and (bridge() or swim)
                self.has_bridge(state),
            "Hotel Room - Hotel Backroom Coin": lambda state:
                #coin17
                #logic: Hotel Room and coffee and sword
                state.has("ItemCoffee", self.player) and self.has_sword(state),
            "Hotel Room - Drill Coin": lambda state:
                #coin18
                #logic: Hotel Room and sword and bridge() and pressPass
                self.has_sword(state) and self.has_bridge(state) and state.has("ItemPressPass", self.player),
            "Hotel Room - Crow Heart": lambda state:
                #heartPiece5
                #logic: Hotel Room and sword and glove and coffee
                self.has_sword(state) and state.has("ItemGlove", self.player) and state.has("ItemCoffee", self.player),
            "Hotel Room - Dog Heart": lambda state:
                #heartPiece6
                #logic: Hotel Room and sword and glove and basement
                self.has_sword(state) and state.has("ItemGlove", self.player) and state.has("ItemBasement", self.player),
                #this logic changes if i rando the bone, don't think i will though
            "Hotel Room - Cooler Tentacle": lambda state:
                #tentacle7
                #logic: Hotel Room and sword and pressPass
                self.has_sword(state) and state.has("ItemPressPass", self.player),
                #alt logic: through underground and loading dock without pass but likely req shoes

        #Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                #tentacle6
                #logic: Island Shack and sword and basementKey and (swim or throw)
                self.has_sword(state) and state.has("ItemBasement", self.player) and   (state.has("ItemSwim", self.player) 
                                                                                        or state.has("ItemThrow", self.player)),

        #Underground Tent
            "Underground Tent - ItemTrophy": lambda state: True,
                #logic: Underground Tent

        #Undefined
            #"REGION - ItemCamera": lambda state: False,
                #logic: unwritten/unknown

            "REGION - itemMegaSword": lambda state: 
                self.has_sword(state) and state.has("ItemWateringCan", self.player) and self.has_bridge(state) and state.has("ItemPressPass", self.player)
            ,
                #logic: unwritten/unknown
            "REGION - ItemBrokenSword": lambda state: True,
                #logic: unwritten/unknown
            "Fight the Boss": lambda state: 
                state.has("ItemMegaSword", self.player)
        }

    def has_sword(self, state) -> bool:
        return state.has_any({"ItemBrokenSword", "ItemMegaSword", "Progressive Sword"}, self.player)
    def has_darkroom(self, state) -> bool:
        return state.has_any({"ItemFlashLight"}, self.player)
    def has_savedResidents(self, state) -> bool:
        return state.has_any({"ItemBrokenSword", "itemMegaSword", "Progressive Sword"}, self.player)
    def has_bridge(self, state) -> bool:
        return (has_darkroom(state) and has_sword(state) and state.has_any({"ItemThrow"}, self.player)) or state.has_any({"ItemSwim"}, self.player)
        #needs to be revisited when i know if the bomb room is a darkroom
    def has_madeboat(self, state) -> bool:
        return state.has_any({"ItemBoat"}, self.player) and state.has_any({"ItemWateringCan"}, self.player)
        #needs to be revisited when i'm sure what spawns boatman
    def can_openChest(self, state) -> bool:
        return state.has_any({"ItemWateringCan"}, self.player) or has_sword(state)
        #need to double check what can all open chests
        #TODO: apply this

    def get_coins(self, state, count: int) -> bool:
        return state.count("Coin", self.player) >= count
    def get_tentacles(self, state, count: int) -> bool:
        return state.count("Tentacle", self.player) >= count

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player)

        #existing Pseudoregalia gomode/completion logic, to copy later if needed
        # set_rule(multiworld.get_location("D S T RT ED M M O   Y", self.player), lambda state:
        #          state.has_all({
        #              "Major Key - Empty Bailey",
        #              "Major Key - The Underbelly",
        #              "Major Key - Tower Remains",
        #              "Major Key - Sansa Keep",
        #              "Major Key - Twilight Theatre",
        #          }, self.player))
        # multiworld.completion_condition[self.player] = lambda state: Ttate.has(
        #     "Something Worth Being Awake For", self.player)
