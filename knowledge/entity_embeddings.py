# Local imports
from rag.embeddings import embed_text


def build_entity_embeddings(graph):
    """Generate embeddings for all graph entities."""

    embeddings = []

    # Process graph nodes
    for node, data in graph.nodes(data=True):

        # Ignore chunk nodes
        if data["node_type"] != "entity":
            continue

        embeddings.append(
            {
                "name": node,
                "embedding": embed_text(node).tolist(),
            }
        )

    return embeddings
