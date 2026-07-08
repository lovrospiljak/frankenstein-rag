import faiss
import numpy as np

from rag.embeddings import embed_text


def load_index(index_path):
    """
    Load the FAISS vector index from disk.
    """
    return faiss.read_index(index_path)


def search(query, index, embeddings, k=5):
    """
    Retrieve the k most relevant chunks for a query.
    """

    # Convert the query into an embedding
    query_vector = embed_text(query)

    # FAISS expects a 2D float32 NumPy array
    query_vector = np.array(
        [query_vector],
        dtype="float32",
    )

    # Search the vector index
    scores, indices = index.search(query_vector, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        chunk = embeddings[idx]

        results.append(
            {
                "chunk_id": chunk["chunk_id"],
                "section_id": chunk["section_id"],
                "text": chunk["text"],
                "score": float(score),
            }
        )

    return results
