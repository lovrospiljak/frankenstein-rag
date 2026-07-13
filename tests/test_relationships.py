# ----------------------------------------
# Test relationship extraction.
#
# Run:
# python -m tests.test_relationships
# ----------------------------------------

# Local imports
from knowledge.relation_extractor import extract_relationships

from utils.storage import load_json

CHUNKS_PATH = "data/processed/chunks.json"


def main():
    """Extract relationships from the text chunks."""

    # Load the text chunks
    chunks = load_json(CHUNKS_PATH)

    # Extract relationships
    relationships = extract_relationships(chunks)

    print(f"\nFound {len(relationships)} relationships.\n")

    # Display the first 50 relationships
    for relationship in relationships[:50]:

        print(
            f"{relationship.source}"
            f" --{relationship.relation}--> "
            f"{relationship.target}"
        )


if __name__ == "__main__":
    main()
