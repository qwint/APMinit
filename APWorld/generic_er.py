# if you see me referencing a field of Entrance or Region that doesn't exist...
# assume I'm proposing to add it.
import random
import queue
from enum import IntEnum, IntFlag
from typing import Any, Callable, Dict, Iterable, Iterator, List, NamedTuple, Optional, Set, Tuple, TypedDict, Union, \
    Type, ClassVar
from BaseClasses import CollectionState, Region, MultiWorld, Entrance

class EntranceType(IntEnum):
    # A transition that can be a physical exit to a scene, but is not normally an entrance 
    # (because the other side is ONE_WAY_OUT). It may or may not be possible to use it an
    # entrance to a scene depending on world and client implementation.
    ONE_WAY_IN = 0
    # A transition that can be a physical entrance to a scene, but is impossible to use as
    # an exit.
    ONE_WAY_OUT = 1
    # A transition that is normally both an entrance and exit to a scene.
    TWO_WAY = 2

class ER_Entrance(Entrance):
    # access_rule: Callable[[CollectionState], bool] = staticmethod(lambda state: True)
    # hide_path: bool = False
    # player: int
    # name: str
    # parent_region: Optional[Region]
    # connected_region: Optional[Region] = None
    # # LttP specific, TODO: should make a LttPEntrance
    # addresses = None
    # target = None
    group_name: str
    entrance_type: EntranceType = 2
    # the set of regions which must be placed prior to pairing off this entrance. used
    # for "gate and switch" use cases where there is some non-item requirement in another
    # region which much be fulfilled before the entrance is actually accessible
    #
    # footnote 1: in theory if your requirements are events this is not needed, but should 
    #             reduce the risk of generation failures due to bad entrance randomization)
    # footnote 2: this could default to empty set to make is_valid_source_transition less
    #             awkward but let's not create sets unnecessarily
    er_required_regions: Set[str]
    # to be computed and stored by ER algorithm
    is_dead_end: bool

    def __init__(self, player: int, name: str = '', parent: Region = None):
        super().__init__(player, name, parent)
        self.er_required_regions = set()

    # def can_reach(self, state: CollectionState) -> bool:
    #     if self.parent_region.can_reach(state) and self.access_rule(state):
    #         if not self.hide_path and not self in state.path:
    #             state.path[self] = (self.name, state.path.get(self.parent_region, (self.parent_region.name, None)))
    #         return True

    #     return False

    # def connect(self, region: Region, addresses: Any = None, target: Any = None) -> None:
    #     self.connected_region = region
    #     self.target = target
    #     self.addresses = addresses
    #     region.entrances.append(self)

    # def __repr__(self):
    #     return self.__str__()

    # def __str__(self):
    #     world = self.parent_region.multiworld if self.parent_region else None
    #     return world.get_name_string_for_object(self) if world else f'{self.name} (Player {self.player})'

    def is_valid_source_transition(self, placed_regions: Set[str]) -> bool:
        """
        Determines whether this is a valid source transition, that is, whether
        the entrance randomizer is allows to pair it off to any another Entrance.

        :param placed_regions: The names of the set of regions that have already been placed
                               by the entrance randomizer.
        """
        return not self.er_required_regions or er_gate_required_regions <= placed_regions

    def can_connect_to(self, other: "Entrance", group_one_ways: bool, allow_self_loops: bool) -> bool:
        """
        Determines whether a given Entrance is a valid target transition, that is, whether
        the entrance randomizer is allowed to pair this entrance off to that entrance

        :param other: The proposed Entrance to connect to.
        :param group_one_ways: Whether to enforce that ONE_WAY_IN transitions must pair
                               with ONE_WAY_OUT transitions
        :param allow_self_loops: Whether to allow an entrance to connect to itself.
        """
        if self.entrance_type == EntranceType.ONE_WAY_OUT:
            raise RuntimeError("can_connect_to should not be called on ONE_WAY_OUT"
                + "Entrances as they are never valid source transitions")

        one_way_type_matches = True
        if group_one_ways:
            required_target_type = (EntranceType.ONE_WAY_OUT 
                if self.entrance_type == EntranceType.ONE_WAY_IN
                else EntranceType.TWO_WAY)
            one_way_type_matches = other.entrance_type == required_target_type
        return one_way_type_matches and (allow_self_loops or self.name != other.name)

class GroupLookup:
    _lookup: {}

    def __init__(self):

        self._lookup = {}
        pass

    def __bool__(self):
        return bool(self._lookup)

    def add(self, entrance: ER_Entrance) -> None:
        group = self._lookup.setdefault(entrance.group_name, [])
        group.append(entrance)

    def remove(self, entrance: ER_Entrance) -> None:
        group = self._lookup[entrance.group_name]
        group.remove(entrance)
        # if not group:
        #     del self._lookup[entrance.group_name]

    def get_group(self, group_name: str) -> Iterable[ER_Entrance]:
        return self._lookup.get(group_name, [])

class EntranceLookup:
    random: random.Random
    dead_ends: GroupLookup # group name to entrances
    non_dead_ends: GroupLookup

    def __init__(self, random: random.Random):
        self.random = random
        self.dead_ends = GroupLookup()
        self.non_dead_ends = GroupLookup()

    def add(self, entrance: ER_Entrance, dead_end: bool) -> None:
        lookup = self.dead_ends if dead_end else self.non_dead_ends
        lookup.add(entrance)

    def remove(self, entrance: ER_Entrance, dead_end: bool) -> None:
        lookup = self.dead_ends if dead_end else self.non_dead_ends
        text = "dead end" if dead_end else "non dead end"
        lookup.remove(entrance)

    def get_targets(self, groups: List[str], dead_end: bool) -> Iterable[ER_Entrance]:
        lookup = self.dead_ends if dead_end else self.non_dead_ends
        ret = [entrance for group in groups for entrance in lookup.get_group(group)]
        self.random.shuffle(ret)
        return ret

class DummyExit(ER_Entrance):
    """
    A simple way to create an Entrance object for ONE_WAY_OUT transitions to be randomized
    by the entrance randomizer. Acts similar to how your other exits will act in the ER, but
    without being considered for logic by normal item fill.
    """

    def __init__(self, name: str, region: Region):
        self.name = name
        self.entrance_type = EntranceType.ONE_WAY_OUT
        self.parent_region = region

# example implementation for the group pairing function for HK to demonstrate how it's supposed to work
def example_get_target_groups(group: str) -> list[str]:
    if self.options.unmatched_room_rando:
        return ["Left", "Right", "Top", "Bottom", "Door"]
    match group:
        case "Left":
            return ["Right", "Door"]
        case "Right":
            return ["Left", "Door"]
        case "Top":
            return ["Bottom"]
        case "Bottom":
            return ["Top"]
        case "Door":
            return ["Left", "Right"]

def randomize_entrances(
        multiworld: MultiWorld, 
        player: int,
        random: random.Random,
        exits_to_randomize: List[ER_Entrance], 
        coupled: bool, 
        group_one_ways: bool,
        get_target_groups: Callable[[str], List[str]]
    ) -> List[tuple[ER_Entrance, ER_Entrance]]:
    """
    Randomizes Entrances for a single world in the multiworld.

    Preconditions:
    1. All of your Regions and all of their exits have been created.
    2. None of your regions' exits are mistakenly labeled as ONE_WAY_OUT
    3. Your Menu region is connected to your starting region.
    4. All the region connections you don't want to randomize are connected, usually
       this is connecting regions within the scene.

    Postconditions:
    All randomizable transitions will have been connected.

    :param multiworld: The multiworld, used to find the Menu region
    :param player: The slot number, used to find the Menu region
    :param random: The Random object used to shuffle entrances
    :param exits_to_randomize: The union of the randomizable exits of your regions, plus any DummyExits 
                         needed to represent one-way transitions
    :param coupled: Whether to couple transitions or not. That is, if the connection A->B is placed,
                    whether the connection B->A should be placed as well (assuming that B is not ONE_WAY_OUT)
    :param group_one_ways: Whether to ensure that ONE_WAY_IN transitions are paired to ONE_WAY_OUT transitions.
                           It is generally safest to set this to True, but can be set to False if your game
                           allows ONE_WAY_IN transitions to be used as the entrance to the room (ie if it is
                           safe to treat them as TWO_WAY).
    """

    results = []
    placed_regions = set()
    available_exits = []
    # exits we'll have to try and connect in a later step, when capping off the connected region graph
    late_exits = []

    entrance_lookup = EntranceLookup(random)

    def traverse_regions_to_new_exits(
            start: Region | ER_Entrance,
            place_regions: bool,
        ) -> Iterable[ER_Entrance]:
        """
        Traverses a region's connected exits to find any newly available randomizable exits
        which stem from that region.

        This is a generator function, so if place_region is true, make sure to iterate it to completion
        for it to actually work correctly.

        :param start: The starting region or entrance to traverse from. If an entrance,
                      doesn't put that entrance in the result
        :param place_regions: Whether to put connecting regions into placed_regions
        """

        visited = set()
        q = queue.Queue()
        starting_entrance_name = None
        if isinstance(start, (ER_Entrance)):
            starting_entrance_name = start.name
            q.put(start.parent_region)
        else:
            q.put(start)

        while not q.empty():
            region = q.get()
            if place_regions:
                placed_regions.add(region.name)
            visited.add(region.name)
            for exit in region.exits:
                if exit.connected_region == None: # only return unconnected (ie randomizable) exits
                    if exit.name != starting_entrance_name:
                        yield exit
                elif exit.connected_region.name not in placed_regions and exit.connected_region.name not in visited:
                    # traverse unseen static connections
                    q.put(exit.connected_region)

    for entrance in exits_to_randomize:
        has_exits = any(exit for exit in traverse_regions_to_new_exits(entrance, False))
        entrance.is_dead_end = not has_exits
        entrance_lookup.add(entrance, entrance.is_dead_end)
        if not coupled:
            # in uncoupled, every TWO_WAY transition can be both a source and a target.
            # additionally, if group_one_ways is false, ONE_WAY_IN can also be a source and a target.
            # double up these transitions in the lookup so they can be randomized accordingly
            if entrance.entrance_type == EntranceType.TWO_WAY or (
                    not group_one_ways and entrance.entrance_type == EntranceType.ONE_WAY_IN):
                entrance_lookup.add(entrance, entrance.is_dead_end)

    # place the starting region. this is doubling the traversal of the start region but that's not
    # the slow part of this algorithm so I don't feel too bad about it (and couldn't figure out how to
    # do it otherwise)
    for exit in traverse_regions_to_new_exits(multiworld.get_region("Menu", player), True):
        entrance_lookup.remove(exit, exit.is_dead_end)
        available_exits.append(exit)

    def pair_exits(
            current_exits: List[ER_Entrance], 
            deadEnd: bool,
        ):
        if deadEnd:
            group_lookup = entrance_lookup.dead_ends
        else:
            group_lookup = entrance_lookup.non_dead_ends

        while bool(current_exits) and bool(group_lookup):
            random.shuffle(current_exits)
            # find a valid source exit
            for i, source_exit in enumerate(current_exits):
                if source_exit.is_valid_source_transition(placed_regions):
                    current_exits.pop(i)
                    break;
            else:
                # TODO: should implement swap for this use case to try and save it.
                raise RuntimeError("Ran out of valid source transitions!")

            # find a random valid target
            target_groups = get_target_groups(source_exit.group_name)
            for target_entrance in entrance_lookup.get_targets(target_groups, deadEnd):
                if source_exit.can_connect_to(target_entrance, group_one_ways, False):
                    entrance_lookup.remove(target_entrance, deadEnd)
                    break;
            else:
                # There were no valid non-dead-end targets for this source, that shouldn't change
                # so throw it in a list to try again later.
                late_exits.append(source_exit)
                continue

            # place the pair and traverse to new exits
            results.append((source_exit, target_entrance))
            # apply coupling - as long as the target entrance is actually able to be used as an entrance,
            # we can couple it. it's possible that target_entrance may be ONE_WAY_IN but whether that is
            # valid is handled by group_one_ways and Entrance.can_connect_to so we don't have to worry about it
            # right at now.
            if coupled and target_entrance.entrance_type != EntranceType.ONE_WAY_OUT:
                results.append((target_entrance, source_exit))

            #temp_exits = traverse_regions_to_new_exits(target_entrance, True)
            for exit in traverse_regions_to_new_exits(target_entrance, True):
                try:
                    entrance_lookup.remove(exit, exit.is_dead_end)
                    current_exits.append(exit)
                except ValueError:
                    print(f"tried to remove {exit.name}, a dead end? {exit.is_dead_end} expecting: {deadEnd}")

    #connect all non_dead_end exits that we can
    print(f"\n1 - available_exits: {available_exits}")
    pair_exits(available_exits, False)

    #connect all dead_end exits that we can
    print(f"\n2 - available_exits: {available_exits}")
    pair_exits(available_exits, True)

    #connect all the previously unconnectable exits
    for entrance in exits_to_randomize:
        for late in late_exits:
            if str(entrance.name) == str(late):
                print(f"adding entrance name: {late}")
                entrance_lookup.add(entrance, entrance.is_dead_end)
    # print(f"\n3 - entrance_lookup DE: {entrance_lookup.get_targets(['water','land'], True)}")
    # print(f"\n3 - entrance_lookup NDE: {entrance_lookup.get_targets(['water','land'], False)}")
    print(f"\n3 - available_exits: {available_exits}")
    pair_exits(available_exits, False)
    pair_exits(available_exits, True)
    # print(f"\n4 - entrance_lookup DE: {entrance_lookup.get_targets(['water','land'], True)}")
    # print(f"\n4 - entrance_lookup NDE: {entrance_lookup.get_targets(['water','land'], False)}")
    print(f"\n4 - available_exits: {available_exits}")
    print(f"\n4 - late_exits: {late_exits}")
    #pair_exits(available_exits, False)
    # print(f"\n5 - entrance_lookup DE: {entrance_lookup.get_targets(['water','land'], True)}")
    # print(f"\n5 - entrance_lookup NDE: {entrance_lookup.get_targets(['water','land'], False)}")
    #print(f"\n5 - available_exits: {available_exits}")

    # here is the stuff that I was too lazy to implement
    # try to place available_exits -> dead ends (ie repeat the above process). Available exits
    #   should be exhausted by now (moved to late exits)
    # try to place late_exits -> dead ends (maybe some of the late exits from the non-dead-end
    #   stage have been saved by placing some dead ends). no need to do shuffling, we're just capping
    #   off branches. If there are unpaired dead ends left at the end of this, then throw or do some swapping
    #   to try and save it.
    # try to place late_exits -> late_exits (cap off anything not capped by a dead end). use a selection with replacement
    #   and allow self-loops in can_connect_to (or don't, and remove that argument, but I thought it was cute lol)
    # if there are any unpaired exits still, then throw or do some swapping to try to save it.
    # actually connect regions
    for source, target in results:
        source.connect(target.parent_region)
    return results;
