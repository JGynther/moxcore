from cards.card import Card, VirtualCard
from cards.utils import should_skip_card
from msgspec import json


def process_scryfall_dump(name: str):
    with open(name) as file:
        content = file.read()
        cards_json = json.decode(content)

    cards: list[VirtualCard] = []
    current_id = 0

    for card_json in cards_json:
        if should_skip_card(card_json):
            continue

        card = Card.from_scryfall_json(card_json)

        for face in card.faces:
            abstraction = VirtualCard.from_card(current_id, card, face)
            cards.append(abstraction)
            current_id += 1

    return cards


def write_cards_json(cards: list[VirtualCard], name="cards.experimental.json"):
    data = {
        "scryfall_base_uri": "https://scryfall.com/card",
        "scryfall_image_base_uri": "https://cards.scryfall.io",
        "cards": cards,
    }

    with open(name, "wb") as file:
        file.write(json.encode(data))
