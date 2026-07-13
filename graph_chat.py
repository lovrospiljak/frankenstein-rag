# Local imports
from knowledge.entity_faiss import load_index
from knowledge.entity_index import build_entity_index
from knowledge.graph_retriever import retrieve_chunks
from knowledge.graph_storage import load_graph

from llm.local import generate_answer

from rag.prompt_builder import build_prompt

from utils.storage import load_json

# ---------------------------------------
# Chat with the knowledge graph.
# ---------------------------------------

GRAPH_PATH = "data/processed/graph.graphml"

ENTITY_FAISS_PATH = "data/processed/entity.index"

ENTITY_LOOKUP_PATH = "data/processed/entity_lookup.json"


def main():
    """Start the GraphRAG chat."""

    print("Loading knowledge graph...")
    graph = load_graph(GRAPH_PATH)

    print("Building entity index...")
    entity_index = build_entity_index(graph)

    print("Loading entity FAISS index...")
    entity_faiss = load_index(
        ENTITY_FAISS_PATH,
    )

    print("Loading entity lookup...")
    entity_lookup = load_json(
        ENTITY_LOOKUP_PATH,
    )

    print("\n=== Frankenstein GraphRAG ===")
    print("Ask me a question about the novel.")
    print("Type 'exit' or 'quit' to close.\n")

    while True:

        question = input("> ").strip()

        if question.lower() in {
            "exit",
            "quit",
        }:

            print("Adios!")
            break

        if not question:
            continue

        # Retrieve relevant chunks
        chunks = retrieve_chunks(
            graph,
            entity_index,
            entity_faiss,
            entity_lookup,
            question,
            k=5,
            verbose=False,
        )

        if not chunks:

            print("\nNo relevant information found.\n")
            continue

        # Build the prompt
        prompt = build_prompt(
            question,
            chunks,
        )

        print("\nThinking...\n")

        # Generate the answer
        answer = generate_answer(
            prompt,
        )

        print("\nAnswer:\n")
        print(answer)

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
