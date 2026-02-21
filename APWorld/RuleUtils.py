from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, HasAny, Rule
from .Options import Darkrooms, Obscure


ignorable_by_obscure = {"options": [OptionFilter(Obscure, Obscure.option_false)], "filtered_resolution": True}
obscure_only_clause = {"options": [OptionFilter(Obscure, Obscure.option_true)], "filtered_resolution": False}


has_megasword = HasAny("ItemMegaSword", "Reverse Progressive Sword") | Has("Progressive Sword", count=3)
has_brokensword = HasAny("ItemBrokenSword", "Progressive Sword") | Has("Reverse Progressive Sword", count=3)
can_pass_boxes = HasAll("has_sword", "ItemGrinder") | Has("ItemCoffee")
can_open_chest = HasAny("has_sword", "ItemWateringCan")

# lt because rulebuilder only short circuits if any filter returns False
has_darkroom0 = Has("ItemFlashLight", options=[OptionFilter(Darkrooms, 0, "lt")], filtered_resolution=True)
has_darkroom1 = Has("ItemFlashLight", options=[OptionFilter(Darkrooms, 1, "lt")], filtered_resolution=True)
has_darkroom2 = Has("ItemFlashLight", options=[OptionFilter(Darkrooms, 2, "lt")], filtered_resolution=True)
has_darkroom3 = Has("ItemFlashLight", options=[OptionFilter(Darkrooms, 3, "lt")], filtered_resolution=True)

completion_rules = {
    "boss_fight": Has("Boss dead"),
    "toilet_goal": has_brokensword & Has("Sword Flushed"),
}


def total_hearts(count: int) -> Rule:
    return Has("HeartPiece", count - 2)
