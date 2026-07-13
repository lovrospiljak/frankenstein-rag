# ----------------------------------------
# Test GraphRAG retrieval.
#
# Run:
# python -m tests.test_graph_retrieval
# ----------------------------------------

# Local imports
from knowledge.entity_index import build_entity_index
from knowledge.graph_retriever import retrieve_chunks
from knowledge.graph_storage import load_graph

GRAPH_PATH = "data/processed/graph.graphml"


def main():
    """Retrieve chunks from the knowledge graph."""

    # Load the graph
    graph = load_graph(GRAPH_PATH)

    # Build the entity index
    entity_index = build_entity_index(graph)

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        # Retrieve relevant chunks
        chunks = retrieve_chunks(
            graph,
            entity_index,
            question,
            k=5,
            verbose=True,
        )

        print()

        print(f"Retrieved {len(chunks)} chunks.\n")

        for chunk in chunks:

            print(f"Score: {chunk['score']}")
            print(f"Chunk: {chunk['chunk_id']}")
            print()

            print(chunk["text"][:500])

            print("\n" + "-" * 80)


if __name__ == "__main__":
    main()
