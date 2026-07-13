# Local imports
from knowledge.entity_matcher import find_matching_nodes
from knowledge.query_parser import extract_query_terms


def retrieve_chunks(
    graph,
    entity_index,
    entity_faiss,
    entity_lookup,
    question,
    k=5,
    verbose=False,
):
    """Retrieve the highest-ranked text chunks from the knowledge graph."""

    query_terms = extract_query_terms(question)

    chunk_scores = {}

    if verbose:
        print("\nQuery terms:")

    # Process query terms
    for term in query_terms:

        entity_name = term.lower()

        if verbose:
            print(f"- {term}")

        matching_nodes = find_matching_nodes(
            entity_index,
            entity_faiss,
            entity_lookup,
            entity_name,
        )

        if not matching_nodes:

            if verbose:
                print("  No matching graph nodes.")

            continue

        if verbose:
            print(f"  Matched: {matching_nodes}")

        # Visit matching entity nodes
        for node_name in matching_nodes:

            # Visit neighboring chunk nodes
            for neighbor in graph.neighbors(node_name):

                node = graph.nodes[neighbor]

                # Ignore non-chunk nodes
                if node["node_type"] != "chunk":
                    continue

                chunk_id = node["chunk_id"]

                # Initialize the chunk score
                if chunk_id not in chunk_scores:

                    chunk_scores[chunk_id] = {
                        "chunk_id": chunk_id,
                        "section_id": node["section_id"],
                        "text": node["text"],
                        "score": 0,
                    }

                # Increase the chunk score
                chunk_scores[chunk_id]["score"] += 1

    # Rank chunks by score
    ranked_chunks = sorted(
        chunk_scores.values(),
        key=lambda chunk: chunk["score"],
        reverse=True,
    )

    return ranked_chunks[:k]
