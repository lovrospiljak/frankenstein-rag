# Third-party imports
import spacy

# Local imports
from knowledge.entities import Entity

from knowledge.entity_normalizer import (
    normalize_entity_name,
)

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Entity types used to build the knowledge graph
GRAPH_ENTITY_TYPES = {
    "PERSON",
    "ORG",
    "GPE",
    "LOC",
    "FAC",
}


def extract_chunk_entities(chunks):
    """Extract named entities from each text chunk."""

    chunk_entities = []

    # Process each text chunk
    for chunk in chunks:

        doc = nlp(chunk["text"])

        entities = []
        seen = set()

        # Extract unique entities from the chunk
        for ent in doc.ents:

            # Ignore unsupported entity types
            if ent.label_ not in GRAPH_ENTITY_TYPES:
                continue

            name = normalize_entity_name(ent)

            # Ignore invalid entity names
            if name is None:
                continue

            # Ignore duplicate entities within the same chunk
            if name in seen:
                continue

            seen.add(name)

            entities.append(
                {
                    "name": name,
                    "type": ent.label_,
                }
            )

        chunk_entities.append(
            {
                "chunk_id": chunk["chunk_id"],
                "entities": entities,
            }
        )

    return chunk_entities


def extract_entities(chunks):
    """Extract unique named entities."""

    chunk_entities = extract_chunk_entities(chunks)

    entities = []
    seen = {}
    entity_id = 0

    # Collect unique entities
    for chunk in chunk_entities:

        for entity in chunk["entities"]:

            name = entity["name"]

            # Ignore entities that were already added
            if name in seen:
                continue

            seen[name] = entity_id

            entities.append(
                Entity(
                    id=entity_id,
                    name=name,
                    type=entity["type"],
                )
            )

            entity_id += 1

    return entities
