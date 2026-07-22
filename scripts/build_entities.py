"""
Build canonical entities.

Pipeline:

chunks
    ↓
extract entities
    ↓
extract chunk entities
    ↓
build entity documents
    ↓
build embeddings
    ↓
cluster aliases
    ↓
choose canonical names
    ↓
save canonical entities
"""

from knowledge.extractor import (
    extract_entities,
    extract_chunk_entities,
)

from knowledge.entity_documents import (
    build_entity_documents,
)

from knowledge.entity_embeddings import (
    build_entity_embeddings,
)

from knowledge.entity_clusterer import (
    cluster_entities,
)

from knowledge.entity_canonicalizer import (
    choose_canonical,
)

from knowledge.entities import (
    CanonicalEntity,
)

from knowledge.storage import (
    load_json,
    save_json,
)

# -------------------------------------------------------------

CHUNKS_PATH = "data/processed/chunks.json"

ENTITIES_PATH = "data/processed/entities.json"

DOCUMENTS_PATH = "data/processed/entity_documents.json"

EMBEDDINGS_PATH = "data/processed/entity_embeddings.json"

CANONICAL_PATH = "data/processed/canonical_entities.json"

# -------------------------------------------------------------


def main():

    print("Loading chunks...")

    chunks = load_json(CHUNKS_PATH)

    print(f"Loaded {len(chunks)} chunks.")
    print()

    # ---------------------------------------------------------
    # Extract entities
    # ---------------------------------------------------------

    print("Extracting entities...")

    entities = extract_entities(chunks)

    save_json(
        [entity.__dict__ for entity in entities],
        ENTITIES_PATH,
    )

    print(f"Found {len(entities)} unique entities.")
    print()

    # ---------------------------------------------------------
    # Extract chunk entities
    # ---------------------------------------------------------

    print("Building chunk entity index...")

    chunk_entities = extract_chunk_entities(
        chunks,
    )

    print(f"{len(chunk_entities)} chunks contain entities.")
    print()

    # ---------------------------------------------------------
    # Build contextual documents
    # ---------------------------------------------------------

    print("Building entity documents...")

    documents = build_entity_documents(
        chunks,
        chunk_entities,
        [entity.__dict__ for entity in entities],
        max_chunks=5,
    )

    save_json(
        documents,
        DOCUMENTS_PATH,
    )

    print(f"Built {len(documents)} entity documents.")
    print()

    # ---------------------------------------------------------
    # Generate embeddings
    # ---------------------------------------------------------

    print("Generating embeddings...")

    embeddings = build_entity_embeddings(
        documents,
    )

    save_json(
        embeddings,
        EMBEDDINGS_PATH,
    )

    print(f"Generated {len(embeddings)} embeddings.")
    print()

    # ---------------------------------------------------------
    # Merge entity metadata + embeddings
    # ---------------------------------------------------------

    merged = []

    embedding_lookup = {embedding["id"]: embedding for embedding in embeddings}

    for entity in entities:

        embedding = embedding_lookup.get(entity.id)

        if embedding is None:
            continue

        merged.append(
            {
                "id": entity.id,
                "name": entity.name,
                "type": entity.type,
                "embedding": embedding["embedding"],
            }
        )

    print(f"Prepared {len(merged)} entities for clustering.")
    print()

    # ---------------------------------------------------------
    # Cluster aliases
    # ---------------------------------------------------------

    print("Clustering similar entities...")

    clusters = cluster_entities(
        merged,
        threshold=0.88,
    )

    print(f"Found {len(clusters)} clusters.")
    print()

    # ---------------------------------------------------------
    # Build canonical entities
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    save_json(
        [entity.__dict__ for entity in canonical_entities],
        CANONICAL_PATH,
    )

    print(f"Saved {len(canonical_entities)} canonical entities.")
    print(f"Output: {CANONICAL_PATH}")


if __name__ == "__main__":
    main()
