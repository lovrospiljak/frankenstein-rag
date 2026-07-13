# Local imports
from knowledge.entity_faiss import search_entities
from knowledge.entity_index import IGNORED_TOKENS

from rag.embeddings import embed_text


def find_matching_nodes(
    entity_index,
    entity_faiss,
    entity_lookup,
    query_term,
    semantic_k=3,
):
    """Find graph nodes matching a query term."""

    matches = []

    query = query_term.lower()

    # ----------------------------------
    # 1. Exact match
    # ----------------------------------

    if query in entity_index:

        matches.extend(entity_index[query])

    # ----------------------------------
    # 2. Token match
    # ----------------------------------

    for token in query.split():

        if token in IGNORED_TOKENS:
            continue

        if token not in entity_index:
            continue

        matches.extend(entity_index[token])

    # Return lexical matches immediately
    if matches:

        return list(dict.fromkeys(matches))

    # ----------------------------------
    # 3. Semantic match
    # ----------------------------------

    query_embedding = embed_text(
        query_term,
    )

    results = search_entities(
        query_embedding,
        entity_faiss,
        entity_lookup,
        k=semantic_k,
    )

    for result in results:

        matches.append(result["name"])

    return list(dict.fromkeys(matches))
