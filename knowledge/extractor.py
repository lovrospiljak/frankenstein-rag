# Third-party import
import spacy

# Local import
from knowledge.entities import Entity

# Load the English Natural Language Processing (NLP) model once
nlp = spacy.load("en_core_web_sm")

# Supported named entity types
SUPPORTED_TYPES = {
    "PERSON",
    "ORG",
    "GPE",
    "LOC",
    "FAC",
}


def extract_entities(chunks):
    """Extract unique named entities from text chunks."""

    entities = []
    seen = set()
    entity_id = 0

    # Process each text chunk
    for chunk in chunks:

        # Run Named Entity Recognition
        doc = nlp(chunk["text"])

        # Process each detected entity
        for ent in doc.ents:

            # Ignore unsupported entity types
            if ent.label_ not in SUPPORTED_TYPES:
                continue

            # Create a unique key for duplicate detection
            key = (ent.text.lower(), ent.label_)

            # Skip duplicate entities
            if key in seen:
                continue

            seen.add(key)

            # Store the extracted entity
            entities.append(
                Entity(
                    id=entity_id,
                    name=ent.text,
                    type=ent.label_,
                )
            )

            entity_id += 1

    return entities


def extract_chunk_entities(chunks):
    """Extract named entities for every text chunk."""

    # Result list
    chunk_entities = []

    # Process each text chunk
    for chunk in chunks:

        # Run Named Entity Recognition
        doc = nlp(chunk["text"])

        entities = []

        # Process each detected entity
        for ent in doc.ents:

            # Ignore unsupported entity types
            if ent.label not in SUPPORTED_TYPES:
                continue

            # Store the entity found in the current chunk
            entities.append(
                {
                    "name": ent.text.strip(),
                    "type": ent.label_,
                }
            )

        # Store all entities belonging to the current chunk
        chunk_entities.append(
            {
                "chunk_id": chunk["chunk_id"],
                "entities": entities,
            }
        )

        return chunk_entities
