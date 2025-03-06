import re

from mox.data_types import Ability, Category
from mox.effects import parse_effects


def parse_ability(input: str, is_spell: bool) -> Ability:
    category: Category = Category.STATIC
    cost: str | None = None
    trigger: str | None = None

    match input:
        case _ if re.match(r"^(when|whenever|at)\b", input):
            category = Category.TRIGGERED
            trigger, input = input.split(",", 1)

        case _ if is_activated_ability(input):
            category = Category.ACTIVATED
            cost, input = input.split(":", 1)

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
