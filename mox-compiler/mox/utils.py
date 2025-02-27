from mox.data_types import Card


def pretty_print(card: Card, print_name=True):
    if print_name:
        print(card.name)
        print("--")

    print("TYPE", card.type)
    print("KEYWORDS", card.keywords)

    for ability in card.abilities:
        print(ability.category, ability.cost or "", ability.trigger or "")
        print("│")

        for index, effect in enumerate(ability.effects):
            is_more = index + 1 < len(ability.effects)

            print(f"{'├' if is_more else '└'}─ {effect.type}")
            print(f"{'│' if is_more else ' '}  ├──[text]        {effect.text}")
            print(f"{'│' if is_more else ' '}  ├──[target]      {effect.target}")
            print(f"{'│' if is_more else ' '}  ├──[condition]   {effect.condition}")
            print(f"{'│' if is_more else ' '}  ├──[source]      {effect.source}")
            print(f"{'│' if is_more else ' '}  └──[destination] {effect.destination}")
            print("│" if is_more else "")

    print()
