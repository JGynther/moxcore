from collections import defaultdict
from itertools import count

import faiss
import torch
import torch.nn.functional as F
from cards.card import VirtualCard
from mox import Card, parse
from mox.data_types import Ability, Category, Effect, EType, Zone
from search.utils import timer
from sentence_transformers import SentenceTransformer


@timer
def create_embeddings(corpus: list[str], debug=False):
    MODEL = "all-MiniLM-L6-v2"
    model = SentenceTransformer(MODEL, device="mps")
    model.bfloat16()

    # Trying to convert to Tensors here deadlocks (i.e. with convert_to_tensor=True)
    return model.encode(corpus, batch_size=512, normalize_embeddings=True, show_progress_bar=debug)


@timer
def compile_all_seq(cards: list[VirtualCard]):
    return [parse(card.oracle_text, card.name, card.type_line) for card in cards]


def extract_attributes(card: Card, ability: Ability, effect: Effect):
    return (
        # card.keywords,
        category_mapping[ability.category],
        ability.cost,
        etype_mapping[effect.type],
        zone_mapping[effect.source],
        zone_mapping[effect.destination],
    ), [
        ability.trigger or "",
        effect.text,
        effect.target or "",
        effect.condition or "",
    ]


category_mapping = {e: i for i, e in enumerate(Category)}
etype_mapping = {e: i for i, e in enumerate(EType)}
zone_mapping = {e: i for i, e in enumerate(Zone)}


@timer
def extract_all(cards: list[Card]):
    effect_to_card: list[int] = []
    effects = []
    texts_to_encode = []

    for index, card in enumerate(cards):
        for ability in card.abilities:
            for effect in ability.effects:
                effect_to_card.append(index)

                attributes, text = extract_attributes(card, ability, effect)

                effects.append(attributes)
                texts_to_encode.extend(text)

    embeddings = create_embeddings(texts_to_encode, debug=True)

    return (
        effect_to_card,
        torch.tensor(effects, device="mps"),
        torch.from_numpy(embeddings).to("mps"),
    )


@timer
@torch.no_grad()
def stack_embeddings(embeddings: torch.Tensor) -> torch.Tensor:
    NUM_ATTR = 4
    E = embeddings.shape[0] // NUM_ATTR
    D = embeddings.shape[1]

    weights = torch.tensor([0.14, 0.6, 0.13, 0.13], device=embeddings.device).view(1, NUM_ATTR, 1)
    reshaped = embeddings.view(E, NUM_ATTR, D)
    weighted = reshaped * weights
    summed = weighted.sum(dim=1)

    return F.normalize(summed, dim=1)


@timer
@torch.no_grad()
def create_vectors(effects: torch.Tensor, text_sim: torch.Tensor):
    test = torch.cat([effects * 0.5, text_sim * 0.5], dim=1)
    test = F.normalize(test, dim=1)
    return test.cpu().numpy()


@timer
def score_all(cards: list[Card]):
    # These happen on GPU
    effect_to_card, effects, embeddings = extract_all(cards)
    embeddings = stack_embeddings(embeddings)
    vectors = create_vectors(effects, embeddings)

    _, dimensions = vectors.shape
    index = faiss.IndexFlatIP(dimensions)

    # Pyright does not understand faiss types
    index.add(vectors)  # type: ignore
    distances, indices = index.search(vectors, k=25)  # type: ignore

    # Voting baskets via nested dictionaries
    # Essentially dict[card_id, dict[card_id, cosine_similarity]]
    # Each effect votes for cards with cosine similarity
    votes: dict[int, dict[int, float]] = defaultdict(lambda: defaultdict(float))

    for effect_i, index, distance in zip(count(), indices, distances):
        card_id = effect_to_card[effect_i]

        index = index.tolist()
        distance = distance.tolist()

        for j, cosine_sim in zip(index, distance):
            card = effect_to_card[j]

            if not card == card_id:
                if cosine_sim >= 1:
                    # Exact matches should be weighted more heavily
                    cosine_sim = cosine_sim * 2

                votes[card_id][card] += cosine_sim

    _sorted = {
        card_id: sorted(inner.keys(), key=lambda key: inner[key], reverse=True)
        for card_id, inner in votes.items()
    }

    return _sorted
