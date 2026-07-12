# Local imports
from knowledge.extractor import extract_entities
from knowledge.storage import save_entities

from utils.storage import load_json

# -----------------------------------------
# Extract named entities from text chunks.
# -----------------------------------------

CHUNKS_PATH = "data/processed/chunks.json"

OUTPUT_PATH = "data/processed/entities.json"


def main():
    """Extract and save named entities."""

    # Load text chunks
    chunks = load_json(CHUNKS_PATH)

    # Extract named entities
    entities = extract_entities(chunks)

    # Save the extracted entities
    save_entities(
        entities,
        OUTPUT_PATH,
    )

    # Display extraction summary
    print(f"Saved {len(entities)} entities.")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
