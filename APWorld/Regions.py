from typing import NamedTuple, Callable, Dict, List, Optional
from BaseClasses import CollectionState


class RegionExit(NamedTuple):
    region: str
    access_rule: Callable[[CollectionState, int], bool] = lambda state, player: True
    breakable_wall: bool = False


region_table: Dict[str, List[str]] = {
    "Menu": ["Dog House"],
    "Dog House": ["Island Shack", "Desert RV", "Hotel Room"],
    "Island Shack": ["Basement"],
    "Desert RV": ["Factory Main"],
    "Hotel Room": ["Underground Tent","Factory Main"],
    "Factory Main": ["Boss Fight", "Hotel Room"],
    "Underground Tent": [],
    "Basement": [],
    "Boss Fight": []
}
    #there are basement -> place entrances but they are not logically relevant