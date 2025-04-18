import re
import typing as T

symbol_pattern = re.compile(r"{([^}]*)}")


def mana_cost_to_weighted_float(mana_cost: str) -> float:
    mv = 0.0

    for cost in mana_cost.split(","):
        if not (cost := cost.strip()):
            continue

        if match := symbol_pattern.findall(cost):
            for symbol in T.cast(list[str], match):
                match symbol:
                    case "w" | "u" | "b" | "r" | "g":
                        mv += 1.5

                    case symbol if symbol.isdigit():
                        mv += float(symbol)

                    case _:
                        mv += 0.5
        else:
            # Differentiate arbitrary string costs
            # e.g. sacrifice another creature
            mv += 0.5

    return mv
