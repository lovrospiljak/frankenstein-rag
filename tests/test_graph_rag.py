# ------------------------------------
# RUN:
# python -m tests.test_graph_rag
# ------------------------------------

# Local imports
from knowledge.entity_index import build_entity_index
from knowledge.graph_retriever import retrieve_chunks
from knowledge.graph_storage import load_graph

from llm.local import generate_answer

from rag.prompt_builder import build_prompt

GRAPH_PATH = "data/processed/graph.graphml"


def main():
    """Test the complete GraphRAG pipeline."""

    graph = load_graph(GRAPH_PATH)

    entity_index = build_entity_index(graph)

    while True:

        question = input("\nQuestion: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        chunks = retrieve_chunks(
            graph,
            entity_index,
            question,
            k=5,
            verbose=True,
        )

        print(f"\nRetrieved {len(chunks)} chunks.\n")

        prompt = build_prompt(
            question,
            chunks,
        )

        answer = generate_answer(prompt)

        print("\nAnswer:\n")

        print(answer)

        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
