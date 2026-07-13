# Local imports
from knowledge.extractor import extract_chunk_entities
from knowledge.graph_builder import build_graph
from knowledge.graph_storage import save_graph

from utils.storage import load_json

# -----------------------------------------
# Build the knowledge graph.
# -----------------------------------------

CHUNKS_PATH = "data/processed/chunks.json"
GRAPH_PATH = "data/processed/graph.graphml"


def main():
    """Build and save the knowledge graph."""

    # Load the text chunks
    chunks = load_json(CHUNKS_PATH)

    # Extract entities from each chunk
    chunk_entities = extract_chunk_entities(chunks)

    # Build the graph
    graph = build_graph(
        chunk_entities,
        chunks,
    )

    # Save the graph
    save_graph(
        graph,
        GRAPH_PATH,
    )

    # Display build summary
    print()

    print("Knowledge graph built successfully.")

    print()

    print(f"Chunk nodes : {len(chunks)}")
    print(f"Entity nodes: {graph.number_of_nodes() - len(chunks)}")

    print()

    print(f"Total nodes : {graph.number_of_nodes()}")
    print(f"Total edges : {graph.number_of_edges()}")

    print()

    print(f"Output: {GRAPH_PATH}")


if __name__ == "__main__":
    main()
