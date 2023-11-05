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
            "Menu -> Dog House": lambda state: self.region_DogHouse(state),
            "Dog House -> Island Shack": lambda state: 
                (self.has_madeboat(state)) or (state.has("ItemSwim", self.player) and bool(self.world.options.obscure.value)),
                #you can swim from treasure island by baiting the shark, look into option how to add as Obscure else leave it out of logic.
            "Dog House -> Desert RV": lambda state:
                self.region_DesertRV(state),
            "Dog House -> Hotel Room": lambda state: 
                self.region_HotelRoom(state),
            "Island Shack -> Basement": lambda state:
                self.has_sword(state) and state.has("ItemBasement", self.player),
            "Desert RV -> Factory Main": lambda state: 
                self.region_factory_desert(state),
            "Hotel Room -> Underground Tent": lambda state: 
                self.has_sword(state) and self.has_darkroom(state) and state.has("ItemGrinder", self.player),
            "Hotel Room -> Factory Main": lambda state:
                self.region_factory_hotel(state),
            "Factory Main -> Boss Fight": lambda state: 
                self.region_BossFight(state),
            "Factory Main -> Hotel Room": lambda state: 
                self.region_hotel_factory(state),
        }

        self.location_rules = {

        #Dog House
            "Dog House - ItemCoffee": lambda state:
                #logic: Dog House and sword
                self.has_sword(state),
            "Dog House - ItemFlashLight": lambda state:
                #logic: Dog House and ItemKey
                ((self.has_sword(state) or state.has("ItemSwim", self.player)) and state.has("ItemKey", self.player)) or (state.has("ItemSwim", self.player) and bool(self.world.options.obscure.value)),
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
                ((self.can_passBoxes(state) and ((state.has("ItemThrow", self.player) and self.has_sword(state)) or state.has("ItemSwim", self.player)))
                or (self.region_HotelRoom(state) 
                    and (self.has_sword(state) and state.has("ItemGrinder", self.player) and state.has("ItemGlove", self.player))
                    or (self.has_sword(state) and state.has("ItemSwim", self.player) and self.total_hearts(state,4)))) or ((self.region_HotelRoom(state) and state.has("ItemSwim", self.player) and self.total_hearts(state,7)) and bool(self.world.options.obscure.value)),
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
                self.has_sword(state) and self.has_darkroom(state) and self.can_openChest(state) and state.has("ItemSwim", self.player),
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
                #vanilla does require sword because the wateringcan drops while drowing in quicksand
                #coin16
                #logic: Desert RV
            "Desert RV - Dumpster": lambda state:
                #coin19
                #logic: Desert RV and sword
                self.has_sword(state),
            "Desert RV - Temple Heart": lambda state:
                #heartPiece3
                #logic: Desert RV and shoes ?(or grinder)
                state.has("ItemShoes", self.player) and (state.has("ItemFlashLight", self.player)) or (self.has_darkroom(state) and bool(self.world.options.obscure.value)),
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
                state.has("ItemSwim", self.player) and state.has("ItemCoffee", self.player) and self.has_darkroom(state),
            "Hotel Room - Shrub Arena Coin": lambda state:
                #coin11
                #logic: Hotel Room and sword
                self.has_sword(state),
            "Hotel Room - Miner's Chest Coin": lambda state:
                #coin12
                #logic: Hotel Room and sword and grinder 
                self.has_sword(state) and state.has("ItemGrinder", self.player) and self.can_openChest(state) and self.has_darkroom(state),
            "Factory Main - Inside Truck": lambda state: True,
                #coin14
                #logic: Factory access
            "Hotel Room - Queue": lambda state:
                #coin15
                #logic: Hotel Room and (bridge() or swim)
                self.has_bridge(state) or self.region_hotel_factory(state),
            "Hotel Room - Hotel Backroom Coin": lambda state:
                #coin17
                #logic: Hotel Room and coffee and sword
                self.can_passBoxes(state) and self.has_sword(state),
            "Factory Main - Drill Coin": lambda state: self.has_sword(state),
                #coin18
                #logic: Factory access and a sword
            "Hotel Room - Crow Heart": lambda state:
                #heartPiece5
                #logic: Hotel Room and sword and glove and coffee
                self.has_sword(state) and state.has("ItemGlove", self.player) and self.can_passBoxes(state),
            "Hotel Room - Dog Heart": lambda state:
                #heartPiece6
                #logic: Hotel Room and sword and glove and basement
                (self.has_sword(state) and state.has("ItemGlove", self.player) and (self.can_teleport(state) or state.has("ItemSwim", self.player) or state.has("ItemShoes", self.player))) or (self.has_sword(state) and state.has("ItemGlove", self.player) and bool(self.world.options.obscure.value)),
                #with good movemnt can do this in 50s with just sword glove, adding teleport/swim/shoes to give more wiggle room outside obscure logic
                #this logic changes if i rando the bone, don't think i will though
            "Factory Main - Cooler Tentacle": lambda state:
                #tentacle7
                #logic: Hotel Room and sword and pressPass
                self.has_sword(state),
                #alt logic: through underground and loading dock without pass but likely req shoes

        #Island Shack
            "Island Shack - Teleporter Tentacle": lambda state:
                #tentacle6
                #logic: Island Shack and sword and basementKey and swim
                (self.has_sword(state) and state.has("ItemBasement", self.player) and state.has("ItemSwim", self.player) and state.has("ItemCoffee", self.player)) or (self.has_sword(state) and state.has("ItemBasement", self.player) and state.has("ItemSwim", self.player) and bool(self.world.options.obscure.value)),

        #Underground Tent
            "Underground Tent - ItemTrophy": lambda state: 
                #logic: Underground Tent
                state.has("ItemSwim", self.player),
                #may require shoes
            "Dog House - Dolphin Heart": lambda state:
                state.has("ItemWateringCan", self.player),
                #water the dolphin NPC south of the watering can location

        #Undefined

            "Factory Main - ItemMegaSword": lambda state:
                state.has("ItemSwim", self.player) and self.has_sword(state) and state.has("ItemWateringCan", self.player) and state.has("ItemCoffee", self.player) and self.has_darkroom(state),
                #drill shortcut for swordless entry assumed
        }
        # or (self.has_sword(state) and state.has("ItemGlove", self.player) and bool(self.world.options.obscure.value))
        # self.obscure_rules = {
        #     "Dog House - ItemFlashLight": lambda state:
        #         #player can collide with the flashlight from below the lighthouse
        #         state.has("ItemSwim", self.player),
        #     "Dog House - ItemPressPass": lambda state:
        #         (self.region_HotelRoom(state) 
        #             and state.has("ItemSwim", self.player) and self.total_hearts(state,7)),
        #         #good movement through the toxic river can go directly south > west with only taking 6 damage
        #     "Island Shack - Teleporter Tentacle": lambda state:
        #         self.has_sword(state) and state.has("ItemBasement", self.player) and state.has("ItemSwim", self.player),
        #         #a precise attack can hit it from the right teleporter's square
        #     "Hotel Room - Dog Heart": lambda state:
        #         self.has_sword(state) and state.has("ItemGlove", self.player),
        #         #less obscure and more just tight timing
        # }

    def has_sword(self, state) -> bool:
        return state.has_any({"ItemSword","ItemBrokenSword", "ItemMegaSword", "ProgressiveSword"}, self.player)
    def has_darkroom(self, state) -> bool:
        return state.has("ItemFlashLight", self.player) or bool(self.world.options.darkrooms.value)
    def has_savedResidents(self, state) -> bool:
        #can save all the residents to access the hotel roof
        return self.has_sword(state) and state.has("ItemCoffee", self.player) and state.has("ItemGlove", self.player) and (self.has_bridge(state) or self.region_hotel_factory(state))
    def has_bridge(self, state) -> bool:
        return  state.has("ItemSwim", self.player) or (self.has_darkroom(state) and state.has("ItemThrow", self.player) and self.has_sword(state))
        #this is also accessible through the factory in the case that your factory access is desert > sword + grinder and you have press pass, but those are covered by region_hotel_factory when necessary
    def has_madeboat(self, state) -> bool:
        return state.has("ItemBoat", self.player) and state.has("ItemWateringCan", self.player) and state.has("ItemGlove", self.player)
        #boatman requires both the watering trigger and having gloves trigger to be met before he can spawn, take the boatwood and repair the boat
    def has_drillShortcut(self, state) -> bool:
        return  self.has_sword(state) and (self.region_factory_hotel(state) or self.region_factory_desert(state))
        #allows you to get into the factory with enough time to wait for queue

    def can_openChest(self, state) -> bool:
        return state.has("ItemWateringCan", self.player) or self.has_sword(state)
        #need to double check what can all open chests
    def can_passBoxes(self, state) -> bool:
        return state.has("ItemCoffee", self.player) or (self.has_sword(state) and state.has("ItemGrinder", self.player))
    def can_teleport(self, state) -> bool:
        return self.has_madeboat(state) and state.has("ItemBasement", self.player) and self.has_sword(state) and state.has("ItemSwim", self.player) or state.has("ItemCoffee", self.player)

    def get_coins(self, state, count: int) -> bool:
        return state.count("Coin", self.player) >= count
    def get_tentacles(self, state, count: int) -> bool:
        return state.count("Tentacle", self.player) >= count
    def total_hearts(self, state, count: int) -> bool:
        return state.count("HeartPiece", self.player) + 2 >= count

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
    def region_factory_hotel(self, state) -> bool:
        return (self.has_sword(state) and state.has("ItemPressPass", self.player) and 
                    ((self.has_darkroom(state) and state.has("ItemThrow", self.player)) or state.has("ItemSwim", self.player))) or (state.has("ItemSwim", self.player) and self.has_darkroom(state))

    def region_factory_desert(self, state) -> bool:
        return  (self.has_sword(state) and state.has("ItemGrinder", self.player)) or (state.has("ItemSwim", self.player) and state.has("ItemCoffee", self.player))
    def region_hotel_factory(self, state) -> bool:
        return  self.region_DesertRV(state) and self.region_factory_desert(state) and self.has_sword(state) and state.has("ItemPressPass", self.player)

    def region_BossFight(self, state) -> bool:
        return state.has("ItemMegaSword", self.player) and self.has_darkroom(state)

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld


        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])
                # if location.name in self.obscure_rules:
                #     add_rule(location, self.obscure_rules[location.name])

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
