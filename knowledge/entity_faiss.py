# Standard library imports
import json

# Third-party imports
import faiss
import numpy as np


def build_index(embeddings):
    """Build a FAISS index from entity embeddings."""

    vectors = np.array(
        [item["embedding"] for item in embeddings],
        dtype=np.float32,
    )

    dimension = vectors.shape[1]

    # Inner product index (works as cosine similarity because
    # the embeddings are already normalized)
    index = faiss.IndexFlatIP(dimension)

    index.add(vectors)

    return index


def save_index(index, path):
    """Save the FAISS index to disk."""

    faiss.write_index(
        index,
        path,
    )


def load_index(path):
    """Load the FAISS index from disk."""

    return faiss.read_index(path)


def save_lookup(embeddings, path):
    """Save entity names without embeddings."""

    lookup = []

    for item in embeddings:

        lookup.append(
            {
                "name": item["name"],
            }
        )

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            lookup,
            f,
            indent=4,
        )


def search_entities(
    query_embedding,
    index,
    lookup,
    k=5,
):
    """Retrieve the most similar entities."""

    query_vector = np.array(
        [query_embedding],
        dtype=np.float32,
    )

    scores, indices = index.search(
        query_vector,
        k,
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0],
    ):

        if idx == -1:
            continue

        results.append(
            {
                "name": lookup[idx]["name"],
                "score": float(score),
            }
        )

    return results
