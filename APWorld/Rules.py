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
            "Dog House -> Island Shack": lambda state: True,
            "Dog House -> Desert RV": lambda state: True,
            "Dog House -> Hotel Room": lambda state: True,
            "Island Shack -> Basement": lambda state: True,
            "Desert RV -> Dog House": lambda state: True,
            "Hotel Room -> Dog House": lambda state: True,
            "Underground Tent -> Dog House": lambda state: True,
            "Basement -> Dog House": lambda state: True,
            "Basement -> Island Shack": lambda state: True,
            "Basement -> Hotel Room": lambda state: True
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
                self.has_sword(state) and self.has_darkroom(state)? and state.has("ItemSwim", self.player),

        #Desert RV
            "Desert RV - ItemThrow": lambda state:
                #logic: Desert RV and sword
                self.has_sword(state),
            "Desert RV - ItemShoes": lambda state:
                #logic: Desert RV and 7 "coin"
                7 "coin",
            "Desert RV - ItemGlove": lambda state:
                #logic: Desert RV and wateringCan
                state.has("ItemWateringCan", self.player),
                #alt logic: Dog House and (sword and glove) or swim
            "Desert RV - ItemTurboInk": lambda state:
                #logic: Desert RV and 8 "tentacle"
                8 "tentacle",
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
                shoes ?(or state.has("ItemGrinder", self.player)),
            "Desert RV - Shop Heart": lambda state:
                #heartPiece4
                #logic: Desert RV and 19 "coin" ?(and Basement) 
                19 "coin" ?(and Basement) ,
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
            "REGION - ItemCamera": lambda state: False,
                #logic: unwritten/unknown

            "REGION - itemMegaSword": lambda state: False,
                #logic: unwritten/unknown
            "REGION - ItemBrokenSword": lambda state: False,
                #logic: unwritten/unknown
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


    #existing Pseudoregalia shortcut methods, to copy later if needed
    # def has_breaker(self, state) -> bool:
    #     return state.has_any({"Dream Breaker", "Progressive Dream Breaker"}, self.player)

    # def has_slide(self, state) -> bool:
    #     return state.has_any({"Slide", "Progressive Slide"}, self.player)

    # def has_plunge(self, state) -> bool:
    #     return state.has("Sunsetter", self.player)

    # def has_gem(self, state) -> bool:
    #     return state.has("Cling Gem", self.player)

    # def can_bounce(self, state) -> bool:
    #     return self.has_breaker(state) and state.has("Ascendant Light", self.player)

    # def can_attack(self, state) -> bool:
    #     """Used where either breaker or sunsetter will work."""
    #     # TODO: Update this to check obscure tricks when logic rework nears completion
    #     return self.has_breaker(state) or state.has("Sunsetter", self.player)

    # def get_kicks(self, state, count: int) -> bool:
    #     kicks: int = 0
    #     if (state.has("Sun Greaves", self.player)):
    #         kicks += 3
    #     kicks += state.count("Heliacal Power", self.player)
    #     kicks += state.count("Air Kick", self.player)
    #     return kicks >= count

    # def kick_or_plunge(self, state, count: int) -> bool:
    #     """Used where one air kick can be replaced with sunsetter. Input is the number of kicks needed without plunge."""
    #     total: int = 0
    #     if (state.has("Sun Greaves", self.player)):
    #         total += 3
    #     if (state.has("Sunsetter", self.player)):
    #         total += 1
    #     total += state.count("Heliacal Power", self.player)
    #     total += state.count("Air Kick", self.player)
    #     return total >= count

    # def has_small_keys(self, state) -> bool:
    #     # TODO: This needs to check for can_attack once breaker can be shuffled
    #     return (state.count("Small Key", self.player) >= 7)

    # def navigate_darkrooms(self, state) -> bool:
    #     # TODO: Update this to check obscure tricks for breaker only when logic rework nears completion
    #     return self.has_breaker(state) or state.has("Ascendant Light", self.player)

    # def can_slidejump(self, state) -> bool:
    #     return (state.has_all({"Slide", "Solar Wind"}, self.player)
    #             or state.count("Progressive Slide", self.player) >= 2)

    # def can_strikebreak(self, state) -> bool:
    #     return (state.has_all({"Dream Breaker", "Strikebreak"}, self.player)
    #             or state.count("Progressive Dream Breaker", self.player) >= 2)

    # def can_soulcutter(self, state) -> bool:
    #     return (state.has_all({"Dream Breaker", "Strikebreak", "Soul Cutter"}, self.player)
    #             or state.count("Progressive Dream Breaker", self.player) >= 3)

    # def knows_obscure(self, state) -> bool:
    #     return bool(self.world.multiworld.obscure_tricks[self.player])

    def set_Minit_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.region_rules:
                    set_rule(entrance, self.region_rules[entrance.name])
            for location in region.locations:
                if location.name in self.location_rules:
                    set_rule(location, self.location_rules[location.name])

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


class MinitNormalRules(MinitRules):
    def __init__(self, world) -> None:
        super().__init__(world)

        self.region_rules.update({
            "Dungeon Mirror -> Dungeon Slide": lambda state:
                self.can_attack(state),
            "Dungeon Slide -> Dungeon Mirror": lambda state:
                self.can_attack(state),
            "Dungeon Slide -> Dungeon Strong Eyes": lambda state:
                self.has_slide(state),
            "Dungeon Slide -> Dungeon Escape Lower": lambda state:
                self.can_attack(state) and self.navigate_darkrooms(state),
            "Dungeon Strong Eyes -> Dungeon Slide": lambda state:
                self.has_slide(state),
            "Dungeon Strong Eyes -> Dungeon => Castle": lambda state:
                self.has_small_keys(state),
            "Dungeon => Castle -> Dungeon Strong Eyes": lambda state:
                self.has_small_keys(state),
            "Dungeon Escape Lower -> Dungeon Slide": lambda state:
                self.can_attack(state),
            "Dungeon Escape Lower -> Dungeon Escape Upper": lambda state:
                self.can_bounce(state)
                or self.get_kicks(state, 1) and self.has_plunge(state)
                or self.get_kicks(state, 3),
            "Dungeon Escape Upper -> Theatre Outside Scythe Corridor": lambda state:
                self.can_bounce(state)
                or self.kick_or_plunge(state, 1)
                or self.has_gem(state),
            "Castle Main -> Dungeon Strong Eyes": lambda state:
                self.has_small_keys(state),
            "Castle Main -> Library Main": lambda state:
                self.has_breaker(state)
                or self.knows_obscure(state) and self.can_attack(state),
            "Castle Main -> Theatre Pillar": lambda state:
                self.has_gem(state) and self.kick_or_plunge(state, 1)
                or self.kick_or_plunge(state, 2),
            "Castle Main -> Castle Spiral Climb": lambda state:
                self.get_kicks(state, 2)
                or self.has_gem(state) and self.has_plunge(state),
            "Castle Spiral Climb -> Castle High Climb": lambda state:
                self.has_gem(state)
                or self.get_kicks(state, 3) and self.has_plunge(state)
                or self.has_breaker(state) and self.get_kicks(state, 1)
                or self.knows_obscure(state) and self.has_plunge(state) and self.get_kicks(state, 1),
            "Castle Spiral Climb -> Castle By Scythe Corridor": lambda state:
                self.has_gem(state),
            "Castle By Scythe Corridor -> Castle Spiral Climb": lambda state:
                self.has_gem(state)
                or self.get_kicks(state, 4) and self.has_plunge(state),
            "Castle By Scythe Corridor -> Castle => Theatre (Front)": lambda state:
                self.has_gem(state) and self.kick_or_plunge(state, 2),
            "Castle By Scythe Corridor -> Castle High Climb": lambda state:
                self.has_gem(state)
                or self.get_kicks(state, 4)
                or self.get_kicks(state, 2) and self.has_plunge(state)
                or self.get_kicks(state, 1) and self.has_plunge(state) and self.can_slidejump(state),
            "Castle => Theatre (Front) -> Castle By Scythe Corridor": lambda state:
                self.has_gem(state)
                or self.can_slidejump(state) and self.get_kicks(state, 1)
                or self.get_kicks(state, 4),
            "Castle => Theatre (Front) -> Castle Moon Room": lambda state:
                self.has_gem(state)
                or self.can_slidejump(state) and self.kick_or_plunge(state, 2),
            "Library Main -> Library Locked": lambda state:
                self.has_small_keys(state),
            "Library Main -> Library Greaves": lambda state:
                self.has_slide(state),
            "Library Main -> Library Top": lambda state:
                self.kick_or_plunge(state, 4)
                or self.knows_obscure(state) and self.get_kicks(state, 1) and self.has_plunge(state),
            "Library Greaves -> Library Top": lambda state:
                self.has_gem(state)
                or self.get_kicks(state, 2),
            "Library Top -> Library Greaves": lambda state:
                self.has_gem(state) and self.kick_or_plunge(state, 1)
                or self.get_kicks(state, 3) and self.has_plunge(state)
                or self.get_kicks(state, 3) and self.can_bounce(state),
        })

        self.location_rules.update({
            "Dilapidated Dungeon - Dark Orbs": lambda state:
                self.has_gem(state) and self.can_bounce(state)
                or self.has_gem(state) and self.kick_or_plunge(state, 3)
                or self.get_kicks(state, 2) and self.can_bounce(state)
                or self.can_slidejump(state) and self.get_kicks(state, 1) and self.can_bounce(state),
            "Dilapidated Dungeon - Past Poles": lambda state:
                self.has_gem(state) and self.kick_or_plunge(state, 1)
                or self.get_kicks(state, 3),
            "Dilapidated Dungeon - Rafters": lambda state:
                self.kick_or_plunge(state, 3)
                or self.knows_obscure(state) and self.can_bounce(state) and self.has_gem(state),
            "Dilapidated Dungeon - Strong Eyes": lambda state:
                self.has_breaker(state)
                or self.knows_obscure(state)
                and (
                    self.has_gem(state) and self.get_kicks(state, 1) and self.has_plunge(state)
                    or self.has_gem(state) and self.get_kicks(state, 3)),
            "Castle Sansa - Floater In Courtyard": lambda state:
                self.can_bounce(state) and self.has_plunge(state)
                or self.can_bounce(state) and self.get_kicks(state, 2)
                or self.has_gem(state) and self.get_kicks(state, 2)
                or self.has_gem(state) and self.has_plunge(state)
                or self.get_kicks(state, 4),
            "Castle Sansa - Locked Door": lambda state:
                self.has_small_keys(state),
            "Castle Sansa - Platform In Main Halls": lambda state:
                self.has_plunge(state)
                or self.has_gem(state)
                or self.get_kicks(state, 2),
            "Castle Sansa - Tall Room Near Wheel Crawlers": lambda state:
                self.has_gem(state) and self.kick_or_plunge(state, 1)
                or self.get_kicks(state, 2),
            "Castle Sansa - Alcove Near Dungeon": lambda state:
                self.has_gem(state) and self.kick_or_plunge(state, 1)
                or self.kick_or_plunge(state, 2),
            "Castle Sansa - Balcony": lambda state:
                self.has_gem(state)
                or self.kick_or_plunge(state, 3)
                or self.can_slidejump(state) and self.kick_or_plunge(state, 2),
            "Castle Sansa - Corner Corridor": lambda state:
                self.has_gem(state)
                or self.get_kicks(state, 4),
            "Castle Sansa - Wheel Crawlers": lambda state:
                self.can_bounce(state)
                or self.has_gem(state)
                or self.get_kicks(state, 2)
                or self.get_kicks(state, 1) and self.can_slidejump(state),
            "Castle Sansa - Alcove Near Scythe Corridor": lambda state:
                self.has_gem(state) and self.get_kicks(state, 1) and self.has_plunge(state)
                or self.kick_or_plunge(state, 4),
            "Castle Sansa - Near Theatre Front": lambda state:
                self.get_kicks(state, 4)
                or self.get_kicks(state, 2) and self.has_plunge(state),
            "Castle Sansa - High Climb From Courtyard": lambda state:
                self.get_kicks(state, 2)
                or self.has_gem(state) and self.has_plunge(state)
                or self.has_breaker(state) and self.get_kicks(state, 1)
                or self.knows_obscure(state) and self.has_plunge(state) and self.get_kicks(state, 1),
            "Listless Library - Sun Greaves": lambda state:
                self.has_breaker(state)
                or self.knows_obscure(state) and self.has_plunge(state),
            "Listless Library - Sun Greaves 1": lambda state:
                self.has_breaker(state)
                or self.knows_obscure(state) and self.has_plunge(state),
            "Listless Library - Sun Greaves 2": lambda state:
                self.has_breaker(state)
                or self.knows_obscure(state) and self.has_plunge(state),
            "Listless Library - Sun Greaves 3": lambda state:
                self.has_breaker(state)
                or self.knows_obscure(state) and self.has_plunge(state),
            "Listless Library - Upper Back": lambda state:
                (self.has_breaker(state) or self.knows_obscure(state) and self.has_plunge(state))
                and (
                    self.has_gem(state) and self.kick_or_plunge(state, 1)
                    or self.kick_or_plunge(state, 2)),
            "Listless Library - Locked Door Across": lambda state:
                self.has_gem(state)
                or self.get_kicks(state, 1)
                or self.can_slidejump(state),
            "Listless Library - Locked Door Left": lambda state:
                self.has_gem(state)
                or self.can_slidejump(state) and self.get_kicks(state, 1)
                or self.kick_or_plunge(state, 3)
        })

    def set_Minit_rules(self) -> None:
        super().set_Minit_rules()
