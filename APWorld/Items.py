from BaseClasses import Item, ItemClassification, MultiWorld
from typing import NamedTuple, Dict, Set, Callable


class MinitItem(Item):
    game = "Minit"


class MinitItemData(NamedTuple):
    code: int = None
    classification: ItemClassification = ItemClassification.filler
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


item_table: Dict[str, MinitItemData] = {
    "Coin": MinitItemData(
        code=60000,
        classification=ItemClassification.progression),
    "HeartPiece": MinitItemData(
        code=60001,
        classification=ItemClassification.useful),
    "Tentacle": MinitItemData(
    #need to double check name
        code=60002,
        classification=ItemClassification.progression),
    "ItemCoffee": MinitItemData(
        code=60003,
        classification=ItemClassification.progression),
    "ItemFlashLight": MinitItemData(
        code=60004,
        classification=ItemClassification.progression),
        #potentially reclassify if darkrooms in logic (when implemented)
    "ItemSwim": MinitItemData(
        code=60005,
        classification=ItemClassification.progression),
    "ItemKey": MinitItemData(
        code=60006,
        classification=ItemClassification.progression),
    "ItemWateringCan": MinitItemData(
        code=60007,
        classification=ItemClassification.progression),
    "ItemThrow": MinitItemData(
        code=60008,
        classification=ItemClassification.progression),
    "ItemShoes": MinitItemData(
        code=60009,
        classification=ItemClassification.progression),
    "ItemGlove": MinitItemData(
        code=60010,
        classification=ItemClassification.progression),
    "ItemBoat": MinitItemData(
        code=60011,
        classification=ItemClassification.progression),
    # "ItemCamera": MinitItemData(
    #     code=60012,
    #     classification=ItemClassification.filler),
    "ItemBasement": MinitItemData(
        code=60013,
        classification=ItemClassification.progression),
    "ItemMegaSword": MinitItemData(
        code=60014,
        classification=ItemClassification.progression),
    "ItemBrokenSword": MinitItemData(
        code=60015,
        classification=ItemClassification.progression),
    "ItemTurboInk": MinitItemData(
        code=60016,
        classification=ItemClassification.filler),
        #this could be helpful, could be filler, but i'd rather have more filler to cut out so i can add extra stuff :)
    "ItemGrinder": MinitItemData(
        code=60017,
        #is filler? no lets you kill boxes with a sword swipe
        classification=ItemClassification.progression),
    "ItemTrophy": MinitItemData(
        code=60018,
        classification=ItemClassification.filler),
    "ItemPressPass": MinitItemData(
        code=60019,
        classification=ItemClassification.progression),
    "ItemSword": MinitItemData(
        code=60020,
        classification=ItemClassification.progression),

   "Boss dead": MinitItemData(
       classification=ItemClassification.progression),

#stolen events from pseudoregalia for gomode and game completion respectivly
#    "Unlocked Door": MinitItemData(
#        classification=ItemClassification.useful),
#
#    "Something Worth Being Awake For": MinitItemData(
#        classification=ItemClassification.progression),
}

item_frequencies = {
    "Coin": 19,
    "HeartPiece": 6,
    "Tentacle": 8
}

item_groups: Dict[str, Set[str]] = {
    "swords": {"ItemBrokenSword",
                   "ItemSword",
                   "ItemMegaSword"},
    "swim": {"ItemSwim"},
    "push": {"ItemCoffee"},
    "cut": {"ItemGlove"},
    "press pass": {"ItemPressPass"},
    "shoes": {"ItemShoes"},
    "watering can": {"ItemWateringCan"},
    "flashlight": {"ItemFlashLight"},
    "lighthouse key": {"ItemKey"},
    "basement key": {"ItemBasement"},
    "grinder": {"ItemGrinder"},
    "throw": {"ItemThrow"},
    "boatwood": {"ItemBoat"},
}