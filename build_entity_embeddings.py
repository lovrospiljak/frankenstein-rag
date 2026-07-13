# Local imports
from knowledge.entity_embeddings import build_entity_embeddings
from knowledge.graph_storage import load_graph

from utils.storage import save_json

# --------------------------------------------
# Generate embeddings for graph entities.
# --------------------------------------------

GRAPH_PATH = "data/processed/graph.graphml"

OUTPUT_PATH = "data/processed/entity_embeddings.json"


def main():
    """Generate and save entity embeddings."""

    # Load the knowledge graph
    graph = load_graph(GRAPH_PATH)

    # Generate entity embeddings
    embeddings = build_entity_embeddings(graph)

    # Save embeddings
    save_json(
        embeddings,
        OUTPUT_PATH,
    )

    # Display summary
    print(f"Embedded {len(embeddings)} entities.")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
