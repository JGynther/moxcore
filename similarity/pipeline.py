from cards.cache import get_scryfall_data_from_cache
from cards.process_dump import write_cards_json
from mox import normalize, pretty_format
from search.bm25 import batch_bm25_search
from search.mox import compile_all_seq, score_all

NULL = "<|NULL|>"
TOP_K = 10

cards = get_scryfall_data_from_cache()

corpus = [normalize(card.oracle_text, card.name) or NULL for card in cards]
results = batch_bm25_search(corpus)

# Mox
compiled = compile_all_seq(cards)
scores = score_all(compiled)

for index, card in enumerate(cards):
    card.neighbours = {}
    card.neighbours["bm25"] = results[index].tolist()[:TOP_K]

    # Some moxc cards don't have effects, and don't get included
    card.neighbours["moxc"] = scores.get(index, [])[:TOP_K]
    card.meta = {
        "moxc_diagnostic": pretty_format(
            compiled[index],
            print_name=False,
        ),
    }


write_cards_json(cards, name="cards.experimental.json")
