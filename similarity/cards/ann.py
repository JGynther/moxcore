from annoy import AnnoyIndex


def create_ann_index(embeddings, dimensions: int):
    # embeddings are normalized so dot product == cosine similarity
    ann_index = AnnoyIndex(dimensions, "dot")

    for index, embedding in enumerate(embeddings):
        ann_index.add_item(index, embedding)

    ann_index.build(n_trees=10, n_jobs=-1)

    return ann_index
