"""
Generate embeddings for entity documents.
"""

from rag.embeddings import embed_text


def build_entity_embeddings(documents):
    """
    Build embeddings for entity documents.

    Parameters
    ----------
    documents : list[dict]

    Returns
    -------
    list[dict]
    """

    embeddings = []

    for document in documents:

        embeddings.append(
            {
                "id": document["id"],
                "name": document["name"],
                "type": document["type"],
                "embedding": embed_text(document["text"]).tolist(),
            }
        )

    return embeddings
