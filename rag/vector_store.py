import faiss
import json
import numpy as np


def build_index(embeddings):
    """
    Creates a FAISS index from embedding vectors.
    """

    vectors = np.array(
        [item["embedding"] for item in embeddings],
        dtype=np.float32,
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(vectors)

    return index


def save_index(index, path):
    faiss.write_index(index, path)


def load_index(path):
    return faiss.read_index(path)


def save_lookup(embeddings, path):
    """
    Saves metadata  without embeddings.
    """

    lookup = []

    for item in embeddings:
        lookup.append(
            {
                "chunk_id": item["chunk_id"],
                "section_id": item["section_id"],
                "text": item["text"],
            }
        )

    with open(path, "w", encoding="utf-8") as f:
        json.dump(lookup, f, indent=4)
