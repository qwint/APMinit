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
    "ItemCamera": MinitItemData(
        code=60012,
        classification=ItemClassification.progression),
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
        #is filler?
        classification=ItemClassification.progression),
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


#    "Boss dead": MinitItemData(
#        classification=ItemClassification.progression),

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

# item groups stolen from pseudoregalia for reuse if/when i need them
# item_groups: Dict[str, Set[str]] = {
#     "major keys": {"Major Key - Empty Bailey",
#                    "Major Key - The Underbelly",
#                    "Major Key - Tower Remains",
#                    "Major Key - Sansa Keep",
#                    "Major Key - Twilight Theatre"},
#     "plunge": {"Sunsetter"},
#     "air kicks": {"Sun Greaves"},
#     "nike kicks": {"Sun Greaves"},
#     "charge": {"Strikebreak"},
#     "projectile": {"Soul Cutter"},
#     "slidejump": {"Solar Wind"},
#     "wallride": {"Cling Gem"},
#     "pogo": {"Ascendant Light"},
#     "floof": {"Professionalism"},
#     "heliacal power": {"Air Kick"},
# }