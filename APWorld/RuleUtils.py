from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasAny, Rule
from .Options import Darkrooms, Obscure


obscure_enabled = OptionFilter(Obscure, Obscure.option_true)


has_megasword = HasAny("ItemMegaSword", "Reverse Progressive Sword") | Has("Progressive Sword", count=3)
has_brokensword = HasAny("ItemBrokenSword", "Progressive Sword") | Has("Reverse Progressive Sword", count=3)
can_pass_boxes = HasAll("has_sword", "ItemGrinder") | Has("ItemCoffee")
can_open_chest = HasAny("has_sword", "ItemWateringCan")

# lt because rulebuilder only short circuits if any filter returns False
has_flashlight = Has("ItemFlashLight")
has_darkroom0 = has_flashlight | OptionFilter(Darkrooms, 0, "ge")
has_darkroom1 = has_flashlight | OptionFilter(Darkrooms, 1, "ge")
has_darkroom2 = has_flashlight | OptionFilter(Darkrooms, 2, "ge")
has_darkroom3 = has_flashlight | OptionFilter(Darkrooms, 3, "ge")

completion_rules = {
    "boss_fight": Has("Boss dead"),
    "toilet_goal": has_brokensword & Has("Sword Flushed"),
}


def total_hearts(count: int) -> Rule:
    return Has("HeartPiece", count - 2)
