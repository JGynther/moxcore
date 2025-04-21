from mox.data_types import Card


def pretty_print(card: Card, print_name=True):
    print(pretty_format(card, print_name))


def pretty_format(card: Card, print_name=True) -> str:
    lines = []

    if print_name:
        lines.append(card.name)
        lines.append("--")

    lines.append(f"TYPE {card.type}")
    lines.append(f"KEYWORDS {card.keywords}")
    lines.append("")

    for ability in card.abilities:
        lines.append(f"{ability.category} {ability.cost or ''} {ability.trigger or ''}".strip())
        lines.append("│")

        for index, effect in enumerate(ability.effects):
            is_more = index + 1 < len(ability.effects)

            branch = "├" if is_more else "└"
            pipe = "│" if is_more else " "

            lines.append(f"{branch}─ {effect.type}")
            lines.append(f"{pipe}  ├──[text]        {effect.text}")
            lines.append(f"{pipe}  ├──[target]      {effect.target}")
            lines.append(f"{pipe}  ├──[condition]   {effect.condition}")
            lines.append(f"{pipe}  ├──[source]      {effect.source}")
            lines.append(f"{pipe}  └──[destination] {effect.destination}")

            if is_more:
                lines.append("│")

        lines.append("")  # trailing newline

    return "\n".join(lines)
