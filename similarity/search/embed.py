import re

from sentence_transformers import SentenceTransformer

from cards.card import VirtualCard

MODEL = "all-MiniLM-L6-v2"  # "llmrails/ember-v1"
model = SentenceTransformer(MODEL, device="mps")


def create_embeddings(corpus: list[str], debug=False):
    return model.encode(corpus, normalize_embeddings=True, show_progress_bar=debug)


def create_card_partial_jsons(cards: list[VirtualCard]) -> list[str]:
    return list(map(construct_embedding_string, cards))


def construct_embedding_string(card: VirtualCard):
    type_line = card.type_line
    oracle_text = card.oracle_text

    text = " ".join([type_line, oracle_text])

    text = text.replace(card.name, "this")  # Remove card name
    text = re.sub(r"\([^)]+\)", "", text)  # Remove reminder text between ()
    text = text.replace("{", "").replace("}", "")

    return text
