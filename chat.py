# Local imports
from llm.local import generate_answer

from rag.prompt_builder import build_prompt
from rag.retriever import load_index, search

from utils.storage import load_json

# ---------------------------------------
# This file does the talking (literally)
# ---------------------------------------

INDEX_PATH = "data/processed/faiss.index"
EMBEDDINGS_PATH = "data/processed/embeddings.json"


def main():
    """Start the interactive RAG application."""

    print("Loading FAISS index...")
    index = load_index(INDEX_PATH)
    embeddings = load_json(EMBEDDINGS_PATH)

    # Display the application header
    print("\n=== Frankenstein RAG ===")
    print("Ask me a question about the novel Frankenstein.")
    print("Type 'exit' or 'quit' to close.\n")

    # Process user questions until the app is closed
    while True:
        question = input("> ").strip()

        # Exit the app
        if question.lower() in {"exit", "quit"}:
            print("Adios!")
            break

        # Ignore empty input
        if not question:
            continue

        # Retrieve the most relevant text chunks
        results = search(
            question,
            index,
            embeddings,
            k=3,
        )

        # Build the prompt for the language model
        prompt = build_prompt(
            question,
            results,
        )

        print("\nThinking...\n")

        # Display the generated answer
        answer = generate_answer(prompt)

        print("\nAnswer:\n")
        print(answer)
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
