import re

condition_pattern = re.compile(r"\bunless\b|\bif\b")


def split_condition_from_effect(effect: str) -> tuple[str | None, str]:
    match condition_pattern.search(effect):
        case None:
            return None, effect

        case match:
            if "," in effect:
                condition, effect = effect.split(",", 1)
            else:
                effect, condition = re.split(rf"\b{match.group(0)}\b", effect, 1)
                condition = match.group(0) + condition

            return condition, effect
