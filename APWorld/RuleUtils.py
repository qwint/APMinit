import Utils


def total_hearts(World, state, count: int) -> bool:
    if World.options.damage_boosts:
        return state.has("HeartPiece", World.player, count - 2)
    else:
        return False


def has_megasword(World, state) -> bool:
    if World.options.progressive_sword == "off":
        return state.has("ItemMegaSword", World.player)
    elif World.options.progressive_sword == "forward_progressive":
        return state.count("Progressive Sword", World.player) >= 3
    elif World.options.progressive_sword == "reverse_progressive":
        return state.count("Reverse Progressive Sword", World.player) >= 1


def has_brokensword(World, state) -> bool:
    if World.options.progressive_sword == "off":
        return state.has("ItemBrokenSword", World.player)
    elif World.options.progressive_sword == "forward_progressive":
        return state.count("Progressive Sword", World.player) >= 1
    elif World.options.progressive_sword == "reverse_progressive":
        return state.count("Reverse Progressive Sword", World.player) >= 3


def has_darkroom(World, state, value) -> bool:
    return (World.options.darkrooms >= value
            or state.has("ItemFlashLight", World.player))


def can_passBoxes(World, state) -> bool:
    return ((
                state.has("has_sword", World.player)
                and state.has("ItemGrinder", World.player))
            or state.has("ItemCoffee", World.player))


def can_openChest(World, state) -> bool:
    return (state.has("has_sword", World.player)
            or state.has("ItemWateringCan", World.player))
