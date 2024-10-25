import re

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

MODEL = "sentence-transformers/all-MiniLM-L12-v2"


def convert_cards_to_embeddable_text(cards):
    data = []
    segment_to_original_index = {}

    for index, card in enumerate(cards):
        oracle = card["oracle"]
        oracle = oracle.replace(card["name"], "this")
        oracle = oracle.lower()

        # FIXME: this should be replaced to use the parser
        oracle = re.sub(r"\([^)]+\)", "", oracle)  # Remove reminder text between ()

        segments = oracle.split("\n")

        for segment in segments:
            segment_to_original_index[len(data)] = index
            data.append(segment)

        segment_to_original_index[len(data)] = index
        data.append(oracle)

        # Replace some symbols with defining text
        # FIXME: Scryfall has full english description for symbols
        # text = text.replace("{T}", "tap")
        # text = text.replace("{Q}", "untap")
        # text = text.replace("{E}", "energy")

    return data, segment_to_original_index


def create_embeddings(text, debug=False):
    if debug:
        try:
            # FIXME: weights_only=false could allow arbitrary code execution
            embeddings = torch.load("checkpoint.pt", weights_only=False)
            embeddings = np.array(embeddings).astype(np.float32)
            dimensions = embeddings[0].shape[0]

            return embeddings, dimensions

        except FileNotFoundError:
            pass

    model = SentenceTransformer(MODEL, device="mps")
    embeddings = model.encode(text, normalize_embeddings=True, show_progress_bar=True)

    embeddings = np.array(embeddings).astype(np.float32)
    dimensions = embeddings[0].shape[0]

    if debug:
        torch.save(embeddings, "checkpoint.pt")

    return embeddings, dimensions
