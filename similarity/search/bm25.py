from itertools import count

from bm25s import BM25, tokenize
from search.utils import timer
from Stemmer import Stemmer


@timer
def batch_bm25_search(corpus: list[str], top_k=50):
    stemmer = Stemmer("english")
    tokens = tokenize(corpus, stopwords="en", stemmer=stemmer)
    retriever = BM25()
    retriever.index(tokens)

    indices, scores = retriever.retrieve(tokens, k=top_k + 1, sorted=False, leave_progress=True)

    result: list[list[tuple[int, float]]] = []

    for index, row_indices, row_scores in zip(count(), indices, scores):
        row = []

        row_indices = row_indices.tolist()
        row_scores = row_scores.tolist()

        for j, score in zip(row_indices, row_scores):
            if index == j:
                continue

            row.append((j, score))

        result.append(row)

    return result
