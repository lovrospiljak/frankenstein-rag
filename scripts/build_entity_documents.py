from knowledge.entity_documents import (
    build_entity_documents,
)

from knowledge.extractor import (
    extract_chunk_entities,
    extract_entities,
)

from utils.storage import (
    load_json,
    save_json,
)

# -------------------------------------------------------

CHUNKS_PATH = "data/processed/chunks.json"

OUTPUT_PATH = "data/processed/entity_documents.json"

# -------------------------------------------------------


def main():

    print("Loading chunks...")

    chunks = load_json(
        CHUNKS_PATH,
    )

    print("Extracting entities...")

    entities = extract_entities(
        chunks,
    )

    print("Extracting mentions...")

    chunk_entities = extract_chunk_entities(
        chunks,
    )

    print("Building entity documents...")

    documents = build_entity_documents(
        chunks,
        chunk_entities,
        entities,
        max_chunks=5,
    )

    save_json(
        documents,
        OUTPUT_PATH,
    )

    print()

    print(f"Saved {len(documents)} entity documents.")


if __name__ == "__main__":
    main()
