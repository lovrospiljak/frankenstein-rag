# Local imports
from knowledge.extractor import extract_entities

from utils.storage import load_json

# -----------------------------
# Test named entity extraction.
# -----------------------------

CHUNKS_PATH = "data/processed/chunks.json"


def main():
    """Extract and display named entities."""

    # Load text chunks
    chunks = load_json(CHUNKS_PATH)

    # Extract named entities
    entities = extract_entities(chunks)

    # Display the extraction summary
    print(f"\nFound {len(entities)} unique entities.\n")

    # Display each extracted entity
    for entity in entities:

        print(f"{entity.id:3} | " f"{entity.type:<8} | " f"{entity.name}")


if __name__ == "__main__":
    main()
