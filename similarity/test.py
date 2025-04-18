from random import choice

from cards.cache import get_scryfall_data_from_cache
from mox import pretty_print
from search.mox import compile_all_seq, score_all


def main():
    cards = get_scryfall_data_from_cache()
    yeet = compile_all_seq(cards)
    votes = score_all(yeet)

    key = 9212  # choice(list(votes.keys()))  # 9212 - black lotus
    card = yeet[key]
    pretty_print(card)

    for card_id in votes[key]:
        pretty_print(yeet[card_id])


if __name__ == "__main__":
    main()
