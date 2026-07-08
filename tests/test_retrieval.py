# ------------------------------------
# RUN:
# python -m tests.test_retrieval
# ------------------------------------

from rag.retriever import (
    load_index,
    search,
)

from utils.storage import load_json

INDEX_PATH = "data/processed/faiss.index"
EMBEDDINGS_PATH = "data/processed/embeddings.json"


def main():

    index = load_index(INDEX_PATH)
    embeddings = load_json(EMBEDDINGS_PATH)

    query = "Who created the creature?"

    results = search(
        query,
        index,
        embeddings,
        k=3,
    )

    print("\nQuestion:")
    print(query)

    print("\n" + "=" * 80)

    for result in results:

        print(f"\nScore: {result['score']:.3f}\n")

        print(result["text"][:500])

        print("\n" + "-" * 80)


if __name__ == "__main__":
    main()
