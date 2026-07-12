# ------------------------------------
# Test the complete Vanilla RAG pipeline.
#
# Run:
# python -m tests.test_rag_pipeline
# ------------------------------------

# Local imports
from llm.local import generate_answer

from rag.prompt_builder import build_prompt

from rag.retriever import (
    load_index,
    search,
)

from utils.storage import load_json

INDEX_PATH = "data/processed/faiss.index"
EMBEDDINGS_PATH = "data/processed/embeddings.json"


def main():
    """Test the complete Vanilla RAG pipeline."""

    # Display the application header
    print("=== Vanilla RAG Pipeline Test ===\n")

    # Load the vector index
    index = load_index(INDEX_PATH)

    # Load chunk metadata
    embeddings = load_json(EMBEDDINGS_PATH)

    # Process user questions until the application is closed
    while True:

        question = input("Question (or 'exit'): ").strip()

        # Exit the application
        if question.lower() in {"exit", "quit"}:
            print("\nAdios!")
            break

        # Retrieve the most relevant chunks
        chunks = search(
            question,
            index,
            embeddings,
            k=3,
        )

        print(f"\nRetrieved {len(chunks)} chunks.\n")

        # Build the prompt for the language model
        prompt = build_prompt(
            question,
            chunks,
        )

        # Generate an answer using the local LLM
        answer = generate_answer(prompt)

        # Display the generated answer
        print("\nAnswer:\n")
        print(answer)
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
