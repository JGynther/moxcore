import re

from mox.cost import mana_cost_to_weighted_float
from mox.data_types import Ability, Category
from mox.effects import parse_effects

trigger_pattern = re.compile(r"^(when|whenever|at)\b")


def parse_ability(input: str, is_spell: bool) -> Ability:
    category: Category = Category.STATIC
    cost = 0
    trigger: str | None = None

    match input:
        case _ if trigger_pattern.search(input):
            category = Category.TRIGGERED
            trigger, input = input.split(",", 1)

        case _ if is_activated_ability(input):
            category = Category.ACTIVATED
            cost_str, input = input.split(":", 1)
            cost = mana_cost_to_weighted_float(cost_str)

        case _:
            if is_spell:
                category = Category.SPELL

    return Ability(category, parse_effects(input), cost, trigger)


def is_activated_ability(input: str) -> bool:
    currently_inside_quotes = False

    for char in input:
        match char:
            case '"':
                currently_inside_quotes = not currently_inside_quotes
            case ":" if not currently_inside_quotes:
                return True

    return False
