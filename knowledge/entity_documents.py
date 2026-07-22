"""
Build contextual documents for every entity.

Each entity document is created by concatenating a few chunks in which the
entity appears. These documents are later embedded for entity resolution.
"""

from collections import defaultdict


def build_entity_documents(
    chunks,
    chunk_entities,
    entities,
    max_chunks=5,
):
    """
    Build one contextual document per entity.

    Parameters
    ----------
    chunks : list[dict]

    chunk_entities : list[dict]

    entities : list[dict]

    max_chunks : int

    Returns
    -------
    list[dict]
    """

    # ---------------------------------------------------------
    # Fast lookup:
    # chunk_id -> chunk
    # ---------------------------------------------------------

    chunk_lookup = {chunk["chunk_id"]: chunk for chunk in chunks}

    # ---------------------------------------------------------
    # entity -> chunk ids
    # ---------------------------------------------------------

    entity_chunks = defaultdict(list)

    for chunk in chunk_entities:

        chunk_id = chunk["chunk_id"]

        for entity in chunk["entities"]:

            name = entity["name"]

            entity_chunks[name].append(chunk_id)

    # ---------------------------------------------------------
    # Build documents
    # ---------------------------------------------------------

    documents = []

    for entity in entities:

        name = entity["name"]

        chunk_ids = entity_chunks.get(name, [])

        # Preserve order
        chunk_ids = sorted(set(chunk_ids))

        texts = []

        for chunk_id in chunk_ids[:max_chunks]:

            if chunk_id not in chunk_lookup:
                continue

            texts.append(chunk_lookup[chunk_id]["text"])

        document = {
            "id": entity["id"],
            "name": name,
            "type": entity["type"],
            "chunk_ids": chunk_ids[:max_chunks],
            "text": "\n\n".join(texts),
        }

        documents.append(document)

    return documents
