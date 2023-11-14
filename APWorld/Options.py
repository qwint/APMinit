from dataclasses import dataclass

from Options import Toggle, Choice, PerGameCommonOptions


class EarlySword(Toggle):
    """Start With a Sword in vanilla Sword Location."""
    display_name = "Early Sword"


class Darkrooms(Toggle):
    """Puts Darkroom navigation without FlashLight in logic."""
    display_name = "Darkrooms"


class Obscure(Toggle):
    """Adds Obscure logic like using only swim to access Island Shack."""
    display_name = "Obscure"


class ProgressiveSword(Choice):
    """Sets the Broken, Basic, and Mega swords to be Progressive Items."""
    """If set to reverse they will increment from Mega to Basic to Broken,"""
    """expected to be used with Toilet Goal."""
    display_name = "ProgressiveSword"
    option_forward_progressive = 0
    option_reverse_progressive = 1
    option_off = 2
    default = 2


class Goal(Choice):
    """Forces the player to win via a specific Goal condition."""
    """Boss is use the Mega Sword to destroy the factory machine"""
    """and beat the boss. Toilet is to aquire the Broken Sword """
    """and drop it into the Factory toilet."""
    display_name = "Goal"
    option_boss_fight = 0
    option_toilet_goal = 1
    option_any_goal = 2
    default = 0


@dataclass
class MinitGameOptions(PerGameCommonOptions):
    starting_sword: EarlySword
    darkrooms: Darkrooms
    obscure: Obscure
    progressive_sword: ProgressiveSword
    chosen_goal: Goal
