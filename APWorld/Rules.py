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
        #TODO fix basement rules
            "Menu -> Dog House": lambda state: self.region_DogHouse(state),
            "Dog House -> Island Shack": lambda state: 
                self.has_madeboat(state),
            "Dog House -> Desert RV": lambda state:
                self.region_DesertRV(state),
            "Dog House -> Hotel Room": lambda state: 
                self.region_HotelRoom(state),
            "Island Shack -> Basement": lambda state:
                self.has_sword(state) and state.has("ItemBasement", self.player),
            "Hotel Room -> Underground Tent": lambda state: 
                self.has_sword(state) and self.has_darkroom(state) and state.has("ItemGrinder", self.player),
            "Hotel Room -> Boss Fight": lambda state: 
                state.has("ItemPressPass", self.player) and self.has_bridge(state) and state.has("ItemMegaSword", self.player) and self.has_darkroom(state),
        }

        self.location_rules = {
        #TODO double check if sword req is only for the line of bushes north or west, and if so make it (sword or swim)

        #Dog House
            "Dog House - ItemCoffee": lambda state:
                #logic: Dog House and sword
                self.has_sword(state),
            "Dog House - ItemFlashLight": lambda state:
                #logic: Dog House and ItemKey
                (self.has_sword(state) or state.has("ItemSwim", self.player)) and state.has("ItemKey", self.player),
            "Dog House - ItemKey": lambda state:
                #logic: Dog House and sword and coffee
                self.has_sword(state) and self.can_passBoxes(state),
                #can swim past the plants, but need to clear the plants by the boxes
            "Dog House - ItemWateringCan": lambda state:
                #logic: Dog House and sword
                self.has_sword(state),
            "Dog house - ItemBoat": lambda state:
                #logic: Dog House and sword and glove
                self.has_sword(state) and state.has("ItemGlove", self.player),
                #can swim to the location but need sword anyway to chop the tree down
            "Dog House - ItemBasement": lambda state:
                #logic: Dog House and sword and glove and madeboat(boatwood and watered guy?)
                self.has_sword(state) and state.has("ItemGlove", self.player) and self.has_madeboat(state),
            "Dog House - ItemPressPass": lambda state:
                #logic: Dog House and sword and coffee and throw
                #alt logic: Hotel Room and sword and grinder and glove
                #alt logic: Hotel Room and canTank(lots)
                (self.has_sword(state) and self.can_passBoxes(state) and state.has("ItemThrow", self.player))
                or (self.region_HotelRoom(state) 
                    and (self.has_sword(state) and state.has("ItemGrinder", self.player) and state.has("ItemGlove", self.player))
                    or (self.has_sword(state) and self.get_hearts(state,2))),
                #you can hit the grass on the output of the toxic river and swim through, may bump to +3 life?
            "Dog House - House Pot Coin": lambda state:
                #coin1
                #logic: Dog House and sword
                self.has_sword(state),
            "Dog House - Sewer Island Coin": lambda state:
                #coin2
                #logic: Dog House and sword and darkroom
                self.has_sword(state) and self.has_darkroom(state) and self.can_openChest(state),
            "Dog House - Sewer Coin": lambda state:
                #coin3
                #logic: Dog House and sword and darkroom
                self.has_sword(state) and self.has_darkroom(state) and self.can_openChest(state),
            "Dog House - Land is Great Coin": lambda state:
                #coin4
                #logic: Dog House and sword and (coffee or swim)
                self.can_openChest(state) and (state.has("ItemSwim", self.player) or (state.has("ItemCoffee", self.player) and self.has_sword(state))),
            "Dog House - Hidden Snake Coin": lambda state:
                #coin5
                #logic: Dog House and sword and darkroom
                (self.has_sword(state) or state.has("ItemSwim", self.player)) and self.has_darkroom(state) and self.can_openChest(state),
            "Dog House - Waterfall Coin": lambda state:
                #coin6
                #logic: Dog House and swim
                state.has("ItemSwim", self.player) and self.can_openChest(state),
            "Dog House - Treasure Island Coin": lambda state:
                #coin7
                #logic: Dog House and swim
                state.has("ItemSwim", self.player) and self.can_openChest(state),
            "Dog House - Plant Heart": lambda state:
                #heartPiece1
                #logic: Dog House and wateringCan
                state.has("ItemWateringCan", self.player),
            "Dog House - Bull Heart": lambda state:
                #heartPiece2
                #logic: Dog House and darkroom() and sword
                (self.has_darkroom(state) and self.has_sword(state))
                or (self.region_DesertRV(state)
                        and self.has_sword(state)),
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
                #alt logic: Dog House and (sword and glove) or swim
                state.has("ItemWateringCan", self.player)
                or (self.region_DogHouse(state) 
                    and (self.has_sword(state) and state.has("ItemGlove", self.player))
                    or state.has("ItemSwim", self.player)),
            "Desert RV - ItemTurboInk": lambda state:
                #logic: Desert RV and 8 "tentacle"
                self.get_tentacles(state, 8) and self.has_darkroom(state),
            "Desert RV - Temple Coin": lambda state: 
                #coin8
                #logic: Desert RV and ?
                self.has_sword(state) and self.has_darkroom(state) and self.can_teleport(state) and self.region_HotelRoom(state),
                #item region implies desert rv access, can teleport implies island shack access, existing implies dog house access, only need to check hotel room access
            "Desert RV - Fire Bat Coin": lambda state:
                #coin9
                #logic: Desert RV and wateringCan
                state.has("ItemWateringCan", self.player) and self.has_darkroom(state) and self.can_openChest(state),
            "Desert RV - Truck Supplies Coin": lambda state:
                #coin10
                #logic: Desert RV and sword
                self.has_sword(state) and self.can_openChest(state),
            "Desert RV - Broken Truck": lambda state:
                #coin13
                #logic: Desert RV and sword
                self.can_openChest(state),
            "Desert RV - Quicksand Coin": lambda state: 
                self.has_sword(state) and self.has_darkroom(state),
                #TODO: check if vanilla drops the watering can when falling through quicksand and fix if it's not vanilla behavior 
                #coin16
                #logic: Desert RV
            "Desert RV - Dumpster": lambda state:
                #coin19
                #logic: Desert RV and sword
                self.has_sword(state),
            "Desert RV - Temple Heart": lambda state:
                #heartPiece3
                #logic: Desert RV and shoes ?(or grinder)
                state.has("ItemShoes", self.player) and self.has_darkroom(state),
            "Desert RV - Shop Heart": lambda state:
                #heartPiece4
                #logic: Desert RV and 19 "coin" and Basement
                self.get_coins(state, 19) and state.has("ItemBasement", self.player),
            "Desert RV - Octopus Tentacle": lambda state:
                #tentacle5
                #logic: Desert RV and sword and swim
                self.has_sword(state) and state.has("ItemSwim", self.player) and self.has_darkroom(state),
            "Desert RV - Beach Tentacle": lambda state:
                #tentacle8
                #logic: Desert RV and sword
                #alt logic: Dog House and sword and swim
                self.has_sword(state)
                or (self.region_DogHouse(state)
                     and self.has_sword(state) and state.has("ItemSwim", self.player)),

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
                state.has("ItemCoffee", self.player) and self.has_darkroom(state),
            "Hotel Room - Shrub Arena Coin": lambda state:
                #coin11
                #logic: Hotel Room and sword
                self.has_sword(state),
            "Hotel Room - Miner's Chest Coin": lambda state:
                #coin12
                #logic: Hotel Room and sword and grinder 
                self.has_sword(state) and state.has("ItemGrinder", self.player) and self.can_openChest(state) and self.has_darkroom(state),
            "Hotel Room - Inside Truck": lambda state:
                #coin14
                #logic: Hotel Room and sword and pressPass and bridge()
                #alt logic: Desert RV and grinder
                (self.has_sword(state) and state.has("ItemPressPass", self.player) and self.has_bridge(state))
                or (self.region_DesertRV(state) 
                        and self.has_sword(state) and state.has("ItemGrinder", self.player)),
            "Hotel Room - Queue": lambda state:
                #coin15
                #logic: Hotel Room and (bridge() or swim)
                self.has_bridge(state) or (self.has_drillShortcut(state) and state.has("ItemPressPass", self.player)),
            "Hotel Room - Hotel Backroom Coin": lambda state:
                #coin17
                #logic: Hotel Room and coffee and sword
                self.can_passBoxes(state) and self.has_sword(state),
            "Hotel Room - Drill Coin": lambda state:
                #coin18
                #logic: Hotel Room and sword and bridge() and pressPass
                self.has_drillShortcut(state),
            "Hotel Room - Crow Heart": lambda state:
                #heartPiece5
                #logic: Hotel Room and sword and glove and coffee
                self.has_sword(state) and state.has("ItemGlove", self.player) and self.can_passBoxes(state),
            "Hotel Room - Dog Heart": lambda state:
                #heartPiece6
                #logic: Hotel Room and sword and glove and basement
                self.has_sword(state) and state.has("ItemGlove", self.player) and self.can_teleport(state),
                #may add 'footing it' to logic too
                #this logic changes if i rando the bone, don't think i will though
            "Hotel Room - Cooler Tentacle": lambda state:
                #tentacle7
                #logic: Hotel Room and sword and pressPass
                (self.has_sword(state) and state.has("ItemPressPass", self.player))
                or (self.region_DesertRV(state)
                     and (self.has_sword(state) and state.has("ItemGrinder", self.player))),
                #alt logic: through underground and loading dock without pass but likely req shoes

        #Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                #tentacle6
                #logic: Island Shack and sword and basementKey and swim
                self.has_sword(state) and state.has("ItemBasement", self.player) and state.has("ItemSwim", self.player) and state.has("ItemCoffee", self.player),

        #Underground Tent
            "Underground Tent - ItemTrophy": lambda state: True,
                #logic: Underground Tent
                #may require shoes

        #Undefined

            "Hotel Room - ItemMegaSword": lambda state: 
                self.has_sword(state) and state.has("ItemWateringCan", self.player) and self.has_bridge(state) and state.has("ItemPressPass", self.player),
                #logic: unwritten/unknown
            "Dog House - ItemSword": lambda state: True,
        }

    def has_sword(self, state) -> bool:
        return state.has_any({"ItemSword","ItemBrokenSword", "ItemMegaSword", "Progressive Sword"}, self.player)
    def has_darkroom(self, state) -> bool:
        return state.has("ItemFlashLight", self.player)
    def has_savedResidents(self, state) -> bool:
        #can save all the residents to access the hotel roof
        return self.has_sword(state) and state.has("ItemCoffee", self.player) and state.has("ItemGlove", self.player) and self.has_bridge(state) 
    def has_bridge(self, state) -> bool:
        return (self.has_darkroom(state) and self.has_sword(state) and state.has("ItemThrow", self.player)) or state.has("ItemSwim", self.player)
    def has_madeboat(self, state) -> bool:
        return state.has("ItemBoat", self.player) and state.has("ItemWateringCan", self.player) and state.has("ItemGlove", self.player)
        #needs to be revisited when i'm sure what spawns boatman                                                #throwing stuff at the wall, i couldn't get the spawn with just boatwood + water and talk to the guy
    def has_drillShortcut(self, state) -> bool:
        return (self.region_HotelRoom(state) and self.has_sword(state) and self.has_bridge(state) and state.has("ItemPressPass", self.player)) or (self.region_DesertRV(state) and (self.has_sword(state) and state.has("ItemGrinder", self.player)))
        #allows you to get into the factory with enough time to wait for queue
        #also why can i not put a newline in here but i can in the region methods??

    def can_openChest(self, state) -> bool:
        return state.has("ItemWateringCan", self.player) or self.has_sword(state)
        #need to double check what can all open chests
    def can_passBoxes(self, state) -> bool:
        return state.has("ItemCoffee", self.player) or (self.has_sword(state) and state.has("ItemGrinder", self.player))
    def can_teleport(self, state) -> bool:
        return self.has_madeboat(state) and state.has("ItemBasement", self.player) and self.has_sword(state)

    def get_coins(self, state, count: int) -> bool:
        return state.count("Coin", self.player) >= count
    def get_tentacles(self, state, count: int) -> bool:
        return state.count("Tentacle", self.player) >= count
    def get_hearts(self, state, count: int) -> bool:
        return state.count("HeartPiece", self.player) >= count

    def region_DogHouse(self, state) -> bool: 
        return True
    def region_DesertRV(self, state) -> bool:
        return (self.region_DogHouse(state)
                    and (self.has_sword(state) and state.has("ItemGlove", self.player)
                    or (self.has_sword(state) or state.has("ItemSwim", self.player)) and self.has_darkroom(state)
                    or state.has("ItemSwim", self.player)))
    def region_HotelRoom(self, state) -> bool:
        return (self.region_DogHouse(state)
                    and (self.has_sword(state) and state.has("ItemGlove", self.player))
                    or state.has("ItemSwim", self.player))

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld


        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])

        #self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss dead", self.player)

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
