from functools import partial

import jax
import jax.numpy as jnp
from bm25s import BM25, tokenize
from Stemmer import Stemmer

from search.utils import timer


def batch_bm25_search(corpus: list[str], top_k=50):
    stemmer = Stemmer("english")
    tokens = tokenize(corpus, stopwords="en", stemmer=stemmer)
    retriever = BM25()
    retriever.index(tokens)

    indices, scores = retriever.retrieve(tokens, k=top_k + 1, sorted=False, leave_progress=True)

    indices = jnp.array(indices)
    scores = jnp.array(scores)

    return remove_self_references(indices, scores, top_k)


@timer
@partial(jax.jit, static_argnames=["top_k"])
def remove_self_references(ids: jnp.ndarray, scores: jnp.ndarray, top_k: int):
    def mask_row(index, ids, scores):
        mask = 1 - jnp.equal(index, ids).astype(int)
        scores = scores * mask
        _, indices = jax.lax.top_k(scores, top_k)
        return jnp.take_along_axis(ids, indices, axis=0)

    rows = jnp.arange(ids.shape[0])
    vectorized = jax.vmap(mask_row, in_axes=(0, 0, 0))

    return vectorized(rows, ids, scores)
