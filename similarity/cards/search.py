from collections import defaultdict
from operator import itemgetter
from typing import Literal

from annoy import AnnoyIndex
from cards.card import Card
from cards.utils import normalize_oracle_text
from numpy import ndarray
from sentence_transformers import SentenceTransformer

CardId = int
CardNeighbor = tuple[int, float]
AnnoyMetric = Literal["angular", "euclidean", "manhattan", "hamming", "dot"]


def cards_to_text_segments(cards: list[Card]):
    segment_to_card_id: dict[int, CardId] = {}
    segments: list[str] = []
    current_segment_id = 0

    for card_id, card in enumerate(cards):
        for face in card.faces:
            for segment in normalize_oracle_text(face).split("\n"):
                segment_to_card_id[current_segment_id] = card_id
                segments.append(segment)
                current_segment_id += 1

    return segments, segment_to_card_id


def generate_embeddings(sentences: list[str], model: SentenceTransformer, debug=False):
    return model.encode(sentences, show_progress_bar=debug)


def create_search_index(embeddings: ndarray, metric: AnnoyMetric = "angular"):
    dimension = embeddings[0].shape[0]
    annoy_index = AnnoyIndex(dimension, metric)

    for index, embedding in enumerate(embeddings):
        annoy_index.add_item(index, embedding)

    annoy_index.build(n_trees=10, n_jobs=-1)

    return annoy_index


def calculate_all_neighbours_for_each(
    segment_to_card_id: dict[int, CardId], annoy_index: AnnoyIndex
):
    results: dict[CardId, list[CardNeighbor]] = defaultdict(list)

    for segment_id in range(annoy_index.get_n_items()):
        card_id = segment_to_card_id[segment_id]

        neighbours, distances = annoy_index.get_nns_by_item(
            segment_id, n=10, include_distances=True
        )

        for segment_id, distance in zip(neighbours, distances):
            neighbour_id = segment_to_card_id[segment_id]
            if card_id != neighbour_id:
                results[card_id] += [(neighbour_id, distance)]

    return results


def filter_to_n_best_neighbours(neighbours: dict[CardId, list[CardNeighbor]], n=10):
    filtered: dict[CardId, list[CardId]] = {}

    for card_id, value in neighbours.items():
        descending_pairs = sorted(value, key=itemgetter(1), reverse=True)

        temp: set[int] = set()

        for id, _ in descending_pairs:
            if id not in temp:
                temp.add(id)

            if len(temp) == n:
                break

        filtered[card_id] = list(temp)

    return filtered
