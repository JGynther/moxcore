from cards.card import Card
from cards.search import (
    calculate_all_neighbours_for_each,
    cards_to_text_segments,
    create_search_index,
    filter_to_n_best_neighbours,
    generate_embeddings,
)
from cards.utils import should_skip_card
from msgspec import json
from sentence_transformers import SentenceTransformer

with open("../oracle-cards-20240927090208.json") as file:
    content = file.read()
    cards_json = json.decode(content)

cards: list[Card] = []
current_id = 0

for card_json in cards_json:
    if should_skip_card(card_json):
        continue

    card = Card.from_scryfall_json(current_id, card_json)
    cards.append(card)
    current_id += 1

model = SentenceTransformer("all-MiniLM-L6-v2", device="mps")

segments, segment_to_card_id = cards_to_text_segments(cards)
embeddings = generate_embeddings(segments, model, debug=True)
search_index = create_search_index(embeddings)
all_neighbours = calculate_all_neighbours_for_each(segment_to_card_id, search_index)
best_neighbours = filter_to_n_best_neighbours(all_neighbours, n=10)

for card_id, neighbours in best_neighbours.items():
    cards[card_id].set_neighbours(neighbours)

data = {
    "scryfall_base_uri": "https://scryfall.com/card",
    "scryfall_image_base_uri": "https://cards.scryfall.io",
    "cards": cards,
}

with open("cards.experimental.json", "wb") as file:
    file.write(json.encode(data))
