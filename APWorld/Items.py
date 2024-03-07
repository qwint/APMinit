from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from typing import NamedTuple, Dict, Set, Callable


class MinitItem(Item):
    game = "Minit"


class MinitItemData(NamedTuple):
    code: int = None
    classification: ItemClassification = ItemClassification.filler
    can_create: Callable[[World, int], bool] = lambda world, player: True


def baseID(delta: int) -> int:
    baseID = 60000
    return baseID + delta


item_table: Dict[str, MinitItemData] = {
    "Coin": MinitItemData(
        code=baseID( 0),
        classification=ItemClassification.progression_skip_balancing),
    "HeartPiece": MinitItemData(
        code=baseID( 1),
        classification=ItemClassification.useful,
        can_create=lambda world, player:
        not bool(world.options.min_hp)),
    "Tentacle": MinitItemData(
        code=baseID( 2),
        classification=ItemClassification.progression),
    "ItemCoffee": MinitItemData(
        code=baseID( 3),
        classification=ItemClassification.progression),
    "ItemFlashLight": MinitItemData(
        code=baseID( 4),
        classification=ItemClassification.progression),
        # potentially reclassify if darkrooms in logic
    "ItemSwim": MinitItemData(
        code=baseID( 5),
        classification=ItemClassification.progression),
    "ItemKey": MinitItemData(
        code=baseID( 6),
        classification=ItemClassification.progression),
    "ItemWateringCan": MinitItemData(
        code=baseID( 7),
        classification=ItemClassification.progression),
    "ItemThrow": MinitItemData(
        code=baseID( 8),
        classification=ItemClassification.progression),
    "ItemShoes": MinitItemData(
        code=baseID( 9),
        classification=ItemClassification.progression),
    "ItemGlove": MinitItemData(
        code=baseID(10),
        classification=ItemClassification.progression),
    "ItemBoat": MinitItemData(
        code=baseID(11),
        classification=ItemClassification.progression),
    # "ItemCamera": MinitItemData(
    #     code=baseID(12),
    #     classification=ItemClassification.filler),
    # camera will never be granted as an item for AP
    "ItemBasement": MinitItemData(
        code=baseID(13),
        classification=ItemClassification.progression),
    "ItemMegaSword": MinitItemData(
        code=baseID(14),
        classification=ItemClassification.progression,
        can_create=lambda world, player:
        world.options.progressive_sword == "off"),
    "ItemBrokenSword": MinitItemData(
        code=baseID(15),
        classification=ItemClassification.progression,
        can_create=lambda world, player:
        world.options.progressive_sword == "off"),
    "ItemTurboInk": MinitItemData(
        code=baseID(16),
        classification=ItemClassification.useful),
    "ItemGrinder": MinitItemData(
        code=baseID(17),
        classification=ItemClassification.progression),
    "ItemTrophy": MinitItemData(
        code=baseID(18),
        classification=ItemClassification.filler),
    "ItemPressPass": MinitItemData(
        code=baseID(19),
        classification=ItemClassification.progression),
    "ItemSword": MinitItemData(
        code=baseID(20),
        classification=ItemClassification.progression,
        can_create=lambda world, player:
        world.options.progressive_sword == "off"),
    "Progressive Sword": MinitItemData(
        code=baseID(21),
        classification=ItemClassification.progression,
        can_create=lambda world, player:
        world.options.progressive_sword == "forward_progressive"),
    "Reverse Progressive Sword": MinitItemData(
        code=baseID(22),
        classification=ItemClassification.progression,
        can_create=lambda world, player:
        world.options.progressive_sword == "reverse_progressive"),

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
