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
        classification=ItemClassification.progression_skip_balancing),
    "HeartPiece": MinitItemData(
        code=60001,
        classification=ItemClassification.useful),
    "Tentacle": MinitItemData(
        code=60002,
        classification=ItemClassification.progression),
    "ItemCoffee": MinitItemData(
        code=60003,
        classification=ItemClassification.progression),
    "ItemFlashLight": MinitItemData(
        code=60004,
        classification=ItemClassification.progression),
        # potentially reclassify if darkrooms in logic
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
    # camera will never be granted as an item for AP
    "ItemBasement": MinitItemData(
        code=60013,
        classification=ItemClassification.progression),
    "ItemMegaSword": MinitItemData(
        code=60014,
        classification=ItemClassification.progression,
        can_create=lambda multiworld, player:
        multiworld.worlds[player].options.progressive_sword.value == 2),
    "ItemBrokenSword": MinitItemData(
        code=60015,
        classification=ItemClassification.progression,
        can_create=lambda multiworld, player:
        multiworld.worlds[player].options.progressive_sword.value == 2),
    "ItemTurboInk": MinitItemData(
        code=60016,
        classification=ItemClassification.useful),
    "ItemGrinder": MinitItemData(
        code=60017,
        classification=ItemClassification.progression),
    "ItemTrophy": MinitItemData(
        code=60018,
        classification=ItemClassification.filler),
    "ItemPressPass": MinitItemData(
        code=60019,
        classification=ItemClassification.progression),
    "ItemSword": MinitItemData(
        code=60020,
        classification=ItemClassification.progression,
        can_create=lambda multiworld, player:
        multiworld.worlds[player].options.progressive_sword.value == 2),
    "Progressive Sword": MinitItemData(
        code=60021,
        classification=ItemClassification.progression,
        can_create=lambda multiworld, player:
        multiworld.worlds[player].options.progressive_sword.value == 0),
    "Reverse Progressive Sword": MinitItemData(
        code=60022,
        classification=ItemClassification.progression,
        can_create=lambda multiworld, player:
        multiworld.worlds[player].options.progressive_sword.value == 1),

    # "Boss dead": MinitItemData(
    #     classification=ItemClassification.progression),
    # added manually in init
}

item_frequencies = {
    "Coin": 19,
    "HeartPiece": 6,
    "Tentacle": 8,
    "Progressive Sword": 3,
    "Reverse Progressive Sword": 3,
}


item_groups: Dict[str, Set[str]] = {
    "swords": {
        "ItemBrokenSword",
        "ItemSword",
        "ItemMegaSword",
        "Progressive Sword",
        "Reverse Progressive Sword",
        },
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
