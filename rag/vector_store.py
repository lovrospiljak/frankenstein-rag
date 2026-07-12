# Standard library import
import json

# Third-party imports
import faiss
import numpy as np


def build_index(embeddings):
    """Build a FAISS index from embedding vectors."""

    # Extract embedding vectors
    vectors = np.array(
        [item["embedding"] for item in embeddings],
        dtype=np.float32,
    )

    # Determine the embedding dimension
    dimension = vectors.shape[1]

    # Create the FAISS index
    index = faiss.IndexFlatIP(dimension)

    # Add vectors to the index
    index.add(vectors)

    return index


def save_index(index, path):
    """Save the FAISS index to disk."""

    faiss.write_index(index, path)


def load_index(path):
    """Load the FAISS index from disk."""

    return faiss.read_index(path)


def save_lookup(embeddings, path):
    """Save chunk metadata  without embedding vectors."""

    lookup = []

    # Extract chunk metadata
    for item in embeddings:
        lookup.append(
            {
                "chunk_id": item["chunk_id"],
                "section_id": item["section_id"],
                "text": item["text"],
            }
        )

    # Save the lookup table
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lookup, f, indent=4)
