import re


def try_to_figure_out_target(effect: str) -> tuple[str | None, str]:
    # Special cases
    for case in ["any target", "each opponent", "target player", "targets"]:
        if case in effect:
            return case, effect.replace(case, "[[target]]")

    match re.search(r"(target|all)[^.,]+", effect):
        case None:
            return None, effect

        case match:
            target = match.group(0).replace("target", "").strip()

            # Arbitrary limit for sanity check
            if not target or len(target.split()) > 6:
                return None, effect

            return target, effect.replace(match.group(0), "[[target]]")
