from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from typing import NamedTuple, Dict, Set, Callable


class MinitItem(Item):
    game = "Minit"


class MinitItemData(NamedTuple):
    code: int = None
    classification: ItemClassification = ItemClassification.filler
    can_create: Callable[[World], bool] = lambda world: True


def baseID(delta: int) -> int:
    baseID = 60000
    return baseID + delta


prog_skip = ItemClassification.progression_skip_balancing
prog = ItemClassification.progression
useful = ItemClassification.useful
filler = ItemClassification.filler


item_table: Dict[str, MinitItemData] = {
    "Coin": MinitItemData(code=baseID(0), classification=prog_skip),
    "HeartPiece": MinitItemData(
        code=baseID(1), classification=useful,
        can_create=lambda world:
        not bool(world.options.min_hp)),
    "Tentacle": MinitItemData(code=baseID(2), classification=prog),
    "ItemCoffee": MinitItemData(code=baseID(3), classification=prog),
    "ItemFlashLight": MinitItemData(code=baseID(4), classification=prog),
    "ItemSwim": MinitItemData(code=baseID(5), classification=prog),
    "ItemKey": MinitItemData(code=baseID(6), classification=prog),
    "ItemWateringCan": MinitItemData(code=baseID(7), classification=prog),
    "ItemThrow": MinitItemData(code=baseID(8), classification=prog),
    "ItemShoes": MinitItemData(code=baseID(9), classification=prog),
    "ItemGlove": MinitItemData(code=baseID(10), classification=prog),
    "ItemBoat": MinitItemData(code=baseID(11), classification=prog),
    # "ItemCamera": MinitItemData(code=baseID(12), classification=filler),
    # camera will never be granted as an item for AP
    "ItemBasement": MinitItemData(code=baseID(13), classification=prog),
    "ItemMegaSword": MinitItemData(
        code=baseID(14), classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "off"),
    "ItemBrokenSword": MinitItemData(
        code=baseID(15), classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "off"),
    "ItemTurboInk": MinitItemData(code=baseID(16), classification=useful),
    "ItemGrinder": MinitItemData(code=baseID(17), classification=prog),
    "ItemTrophy": MinitItemData(code=baseID(18), classification=filler),
    "ItemPressPass": MinitItemData(code=baseID(19), classification=prog),
    "ItemSword": MinitItemData(
        code=baseID(20), classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "off"),
    "Progressive Sword": MinitItemData(
        code=baseID(21), classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "forward_progressive"),
    "Reverse Progressive Sword": MinitItemData(
        code=baseID(22), classification=prog,
        can_create=lambda world:
        world.options.progressive_sword == "reverse_progressive"),

    # "Boss dead": MinitItemData(classification=prog),
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
