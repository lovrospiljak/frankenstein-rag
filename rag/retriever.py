# Third-party imports
import faiss
import numpy as np

# Local import
from rag.embeddings import embed_text


def load_index(index_path):
    """Load the FAISS vector index from disk."""

    return faiss.read_index(index_path)


def search(query, index, chunk_lookup, k=5):
    """Retrieve the k most relevant chunks for a query."""

    # Generate an embedding for the query
    query_vector = embed_text(query)

    # Convert the embedding into the format expected by FAISS
    query_vector = np.array(
        [query_vector],
        dtype="float32",
    )

    # Search the vector index
    scores, indices = index.search(query_vector, k)

    results = []

    # Process the retrieved chunks
    for score, idx in zip(scores[0], indices[0]):

        # Ignore invalid search results
        if idx == -1:
            continue

        chunk = chunk_lookup[idx]

        # Store the retrieved chunk
        results.append(
            {
                "chunk_id": chunk["chunk_id"],
                "section_id": chunk["section_id"],
                "text": chunk["text"],
                "score": float(score),
            }
        )

    return results
