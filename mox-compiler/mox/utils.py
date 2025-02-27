from mox.data_types import Card


def pretty_print(card: Card):
    print(card.name)
    print("KEYWORDS", card.keywords)

    for ability in card.abilities:
        print(ability.category, ability.cost or "", ability.trigger or "")
        for effect in ability.effects:
            print(" -- ", effect)

    print("\n\n")
