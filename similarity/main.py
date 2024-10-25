import msgspec
from cards.ann import create_ann_index
from cards.embedding import convert_cards_to_embeddable_text, create_embeddings
from cards.process_scryfall_dump import process_scryfall_dump

cards = process_scryfall_dump("../oracle-cards-20240927090208.json")
text, index_map = convert_cards_to_embeddable_text(cards)
embeddings, dimensions = create_embeddings(text, debug=True)
ann_index = create_ann_index(embeddings, dimensions)

segment_nn = [[] for _ in cards]

for i in range(ann_index.get_n_items()):
    neighbours, distances = ann_index.get_nns_by_item(i, n=20, include_distances=True)

    card_id = index_map[i]
    for neighbour, distance in zip(neighbours, distances):
        id = index_map[neighbour]
        if not card_id == id:
            segment_nn[card_id].append((id, distance))


def decending_uniques(pairs):
    data = {}

    for index, distance in pairs:
        if index not in data or distance > data[index]:
            data[index] = distance

    return sorted(data.items(), key=lambda x: x[1], reverse=True)


for index, card in enumerate(cards):
    segments = segment_nn[index]
    segments = decending_uniques(segments)
    segments = segments[:10]  # 10 closest neighbours
    card["neighbours"] = [pair[0] for pair in segments]
    card["id"] = index  # FIXME: temp

data = {
    "scryfall_base_uri": "https://scryfall.com/card",
    "scryfall_image_base_uri": "https://cards.scryfall.io",
    "cards": cards,
}

with open("cards.experimental.json", "wb") as file:
    file.write(msgspec.json.encode(data))
