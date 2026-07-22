# Local imports
from knowledge.entity_faiss import (
    build_index,
    save_index,
    save_lookup,
)

from utils.storage import load_json

# --------------------------------------------
# Build a FAISS index for graph entities.
# --------------------------------------------

EMBEDDINGS_PATH = "data/processed/entity_embeddings.json"

INDEX_PATH = "data/processed/entity.index"

LOOKUP_PATH = "data/processed/entity_lookup.json"


def main():
    """Build and save the entity FAISS index."""

    # Load entity embeddings
    embeddings = load_json(
        EMBEDDINGS_PATH,
    )

    # Build the FAISS index
    index = build_index(
        embeddings,
    )

    # Save the FAISS index
    save_index(
        index,
        INDEX_PATH,
    )

    # Save the entity lookup table
    save_lookup(
        embeddings,
        LOOKUP_PATH,
    )

    # Display summary
    print(f"Indexed {len(embeddings)} entities.")
    print(f"Index : {INDEX_PATH}")
    print(f"Lookup: {LOOKUP_PATH}")


if __name__ == "__main__":
    main()
