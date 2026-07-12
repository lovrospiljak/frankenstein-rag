# ------------------------------------
# Test semantic retrieval using FAISS.
#
# Run:
# python -m tests.test_retrieval
# ------------------------------------

# Local imports
from rag.retriever import (
    load_index,
    search,
)

from utils.storage import load_json

INDEX_PATH = "data/processed/faiss.index"
EMBEDDINGS_PATH = "data/processed/embeddings.json"


def main():
    """Retrieve and display the most relevant text chunks."""

    # Load the vector index
    index = load_index(INDEX_PATH)

    # Load chunk metadata
    embeddings = load_json(EMBEDDINGS_PATH)

    # Define the search query
    query = "Who created the creature?"

    # Retrieve the most relevant text chunks
    results = search(
        query,
        index,
        embeddings,
        k=3,
    )

    # Display the search query
    print("\nQuestion:")
    print(query)

    print("\n" + "=" * 80)

    # Display the retrieved chunks
    for result in results:

        print(f"\nScore: {result['score']:.3f}\n")
        print(result["text"][:500])

        print("\n" + "-" * 80)


if __name__ == "__main__":
    main()
