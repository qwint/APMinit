from BaseClasses import Location, MultiWorld
from typing import NamedTuple, Dict, Optional, Callable


class MinitLocationData(NamedTuple):
    region: str
    code: int = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None
    show_in_spoiler: bool = True


location_table = {

    "Dog House - ItemCoffee": MinitLocationData(
        code=CODENUMBER,
        region="Dog House",),
    "Dog House - ItemFlashLight": MinitLocationData(
        code=CODENUMBER,
        region="Dog House",),
    "Hotel Room - ItemSwim": MinitLocationData(
        code=CODENUMBER,
        region="Hotel Room",),
    "REGION - ItemKey": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "Dog House - ItemWateringCan": MinitLocationData(
        code=CODENUMBER,
        region="Dog House",),
    "REGION - ItemThrow": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "Desert RV - ItemShoes": MinitLocationData(
        code=CODENUMBER,
        region="Desert RV",),
    "REGION - ItemGlove": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "Dog house - ItemBoat": MinitLocationData(
        code=CODENUMBER,
        region="Dog house",),
    "REGION - ItemCamera": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - ItemBasement": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - itemMegaSword": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - ItemBrokenSword": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - ItemTurboInk": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - ItemGrinder": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - ItemTrophy": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - itemPressPass": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin01": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin02": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin03": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin04": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin05": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin06": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin07": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin08": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin09": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin10": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin11": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin12": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin13": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin14": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin15": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin16": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin17": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin18": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - coin19": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - heartPiece1": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - heartPiece2": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - heartPiece3": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - heartPiece4": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - heartPiece5": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - heartPiece6": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle1": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle2": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle3": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle4": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle5": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle6": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle7": MinitLocationData(
        code=CODENUMBER,
        region="REGION",),
    "REGION - tentacle8": MinitLocationData(
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