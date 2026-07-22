from knowledge.entity_clusterer import cluster_entities
from knowledge.entity_canonicalizer import choose_canonical
from knowledge.entities import CanonicalEntity

from utils.storage import load_json
from utils.storage import save_json

ENTITIES_PATH = "data/processed/entities.json"

EMBEDDINGS_PATH = "data/processed/entity_embeddings.json"

OUTPUT_PATH = "data/processed/canonical_entities.json"


def main():

    print("Loading entities...")

    entities = load_json(
        ENTITIES_PATH,
    )

    print("Loading embeddings...")

    embeddings = load_json(
        EMBEDDINGS_PATH,
    )

    # ----------------------------------------------------

    merged = []

    for entity, embedding in zip(
        entities,
        embeddings,
    ):

        merged.append(
            {
                "id": entity["id"],
                "name": entity["name"],
                "type": entity["type"],
                "embedding": embedding["embedding"],
            }
        )

    print()

    print(f"{len(merged)} entities loaded.")

    # ----------------------------------------------------

    print()

    print("Clustering...")

    clusters = cluster_entities(
        merged,
        threshold=0.88,
    )

    canonical_entities = []

    for cluster in clusters:

        canonical = choose_canonical(cluster)

        aliases = sorted(
            {
                entity["name"]
                for entity in cluster
                if entity["name"] != canonical["name"]
            }
        )

        canonical_entities.append(
            CanonicalEntity(
                canonical=canonical["name"],
                entity_type=canonical["type"],
                aliases=aliases,
                mention_count=len(cluster),
            )
        )

    print()
    print(f"Saving {len(canonical_entities)} canonical entities...")

    save_json(
        [entity.__dict__ for entity in canonical_entities],
        OUTPUT_PATH,
    )

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
