import Utils


def total_hearts(World, state, count: int) -> bool:
    if World.options.damage_boosts:
        return state.has("HeartPiece", World.player, count - 2)
    else:
        return False


def has_megasword(World, state) -> bool:
    return (state.has_any({
            "ItemMegaSword",
            "Reverse Progressive Sword",
            }, World.player)
            or state.has("Progressive Sword", World.player, 3)
            )


def has_brokensword(World, state) -> bool:
    return (state.has_any({
            "ItemBrokenSword",
            "Progressive Sword",
            }, World.player)
            or state.has("Reverse Progressive Sword", World.player, 3)
            )


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
