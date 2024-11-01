from cards.process_dump import process_scryfall_dump, write_cards_json
from cards.search import (
    calculate_all_neighbours_for_each,
    cards_to_text_segments,
    create_search_index,
    filter_to_n_best_neighbours,
    generate_embeddings,
)
from sentence_transformers import SentenceTransformer

cards = process_scryfall_dump("../oracle-cards-20240927090208.json")

model = SentenceTransformer("all-MiniLM-L12-v2", device="mps")

segments, segment_to_card_id = cards_to_text_segments(cards)
embeddings = generate_embeddings(segments, model, debug=True)
search_index = create_search_index(embeddings)
all_neighbours = calculate_all_neighbours_for_each(segment_to_card_id, search_index)
best_neighbours = filter_to_n_best_neighbours(all_neighbours, n=10)

for card in cards:
    card.neighbours = best_neighbours[card.id]

write_cards_json(cards)
