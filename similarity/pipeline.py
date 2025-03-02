from cards.cache import get_scryfall_data_from_cache
from cards.process_dump import write_cards_json
from cards.utils import normalize_oracle_text
from search.bm25 import batch_bm25_search
from search.embed import create_card_partial_jsons, create_embeddings
from search.rerank import batch_rerank

NULL = "<|NULL|>"
TOP_K = 10

cards = get_scryfall_data_from_cache()
corpus = [normalize_oracle_text(card) or NULL for card in cards]

results = batch_bm25_search(corpus)
embeddings = create_embeddings(create_card_partial_jsons(cards), debug=True)
reranked = batch_rerank(embeddings, results)

for index, card in enumerate(cards):
    card.neighbours = {}
    card.neighbours["bm25"] = results[index].tolist()[:TOP_K]
    card.neighbours["hybrid"] = reranked[index].tolist()[:TOP_K]

write_cards_json(cards, name="cards.experimental.json")
