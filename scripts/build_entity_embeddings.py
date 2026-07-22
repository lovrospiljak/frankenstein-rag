"""
Generate embeddings for canonical entity profiles.
"""

from knowledge.entity_embeddings import build_entity_embeddings

from utils.storage import (
    load_json,
    save_json,
)

INPUT_PATH = "data/processed/entity_profiles.json"

OUTPUT_PATH = "data/processed/entity_embeddings.json"


def main():

    print("Loading entity profiles...")

    profiles = load_json(INPUT_PATH)

    print(f"Loaded {len(profiles)} profiles.")

    print()

    print("Generating embeddings...")

    embeddings = build_entity_embeddings(
        profiles,
    )

    save_json(
        embeddings,
        OUTPUT_PATH,
    )

    print(f"Saved {len(embeddings)} embeddings.")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
