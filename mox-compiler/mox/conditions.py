import re


def split_condition_from_effect(effect: str) -> tuple[str | None, str]:
    match re.search(r"\bunless\b|\bif\b", effect):
        case None:
            return None, effect

        case match:
            if "," in effect:
                condition, effect = effect.split(",", 1)
            else:
                effect, condition = effect.split(match.group(0), 1)
                condition = match.group(0) + condition

            return condition, effect
