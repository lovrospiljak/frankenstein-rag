# ------------------------------------
# RUN:
# python -m tests.test_rag_pipeline
# ------------------------------------

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

    print("=== Frankenstein RAG Pipeline Test ===\n")

    # Load FAISS index
    index = load_index(INDEX_PATH)

    # Load chunk metadata
    embeddings = load_json(EMBEDDINGS_PATH)

    while True:

        question = input("Question (or 'exit'): ").strip()

        if question.lower() in {"exit", "quit"}:
            print("\nAdios!")
            break

        # Retrieve relevant chunks
        chunks = search(
            question,
            index,
            embeddings,
            k=3,
        )

        print(f"\nRetrieved {len(chunks)} chunks.\n")

        # Build RAG prompt
        prompt = build_prompt(
            question,
            chunks,
        )

        # Generate answer
        answer = generate_answer(prompt)

        print("\nAnswer:\n")
        print(answer)
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
