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
    "Desert RV": ["Dog House"],
    "Hotel Room": ["Dog House"],
    "Underground Tent": ["Dog House"],
    "Basement": ["Dog House", "Island Shack", "Hotel Room"]
}