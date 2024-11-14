import jax
import jax.numpy as jnp

from search.utils import timer


@jax.jit
def jax_cos_sim(embeddings: jnp.ndarray, indices: jnp.ndarray):
    similarity = jnp.einsum("ik,ijk->ij", embeddings, embeddings[indices])
    sorted = jnp.argsort(similarity, axis=1, descending=True)
    return jnp.take_along_axis(indices, sorted, axis=1)


@timer
def batch_rerank(embeddings, results):
    return jax_cos_sim(jnp.array(embeddings), jnp.array(results))
