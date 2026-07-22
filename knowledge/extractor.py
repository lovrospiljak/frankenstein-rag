# Third-party imports
import spacy

# Local imports
from knowledge.entities import (
    Entity,
    EntityMention,
)

from knowledge.entity_normalizer import (
    normalize_entity_name,
)

# -------------------------------------------------------------

nlp = spacy.load("en_core_web_sm")

GRAPH_ENTITY_TYPES = {
    "PERSON",
    "ORG",
    "GPE",
    "LOC",
    "FAC",
}

# -------------------------------------------------------------


def extract_entity_mentions(chunks):
    """
    Extract every entity mention from every chunk.

    Returns
    -------
    list[EntityMention]
    """

    mentions = []

    for chunk in chunks:

        doc = nlp(chunk["text"])

        for ent in doc.ents:

            if ent.label_ not in GRAPH_ENTITY_TYPES:
                continue

            name = normalize_entity_name(ent)

            if name is None:
                continue

            mentions.append(
                EntityMention(
                    chunk_id=chunk["chunk_id"],
                    section_id=chunk["section_id"],
                    entity_name=name,
                    entity_type=ent.label_,
                    start=ent.start_char,
                    end=ent.end_char,
                    text=ent.text,
                )
            )

    return mentions


# -------------------------------------------------------------


def extract_chunk_entities(chunks):
    """
    Build a mapping

        chunk_id -> entities
    """

    mentions = extract_entity_mentions(
        chunks,
    )

    chunk_lookup = {}

    for mention in mentions:

        chunk_id = mention.chunk_id

        if chunk_id not in chunk_lookup:

            chunk_lookup[chunk_id] = {
                "chunk_id": chunk_id,
                "entities": [],
            }

        existing = {entity["name"] for entity in chunk_lookup[chunk_id]["entities"]}

        if mention.entity_name in existing:

            continue

        chunk_lookup[chunk_id]["entities"].append(
            {
                "name": mention.entity_name,
                "type": mention.entity_type,
            }
        )

    return list(chunk_lookup.values())


# -------------------------------------------------------------


def extract_entities(chunks):
    """
    Extract unique entities.
    """

    mentions = extract_entity_mentions(
        chunks,
    )

    entities = []

    seen = {}

    entity_id = 0

    for mention in mentions:

        if mention.entity_name in seen:

            continue

        seen[mention.entity_name] = entity_id

        entities.append(
            Entity(
                id=entity_id,
                name=mention.entity_name,
                type=mention.entity_type,
            )
        )

        entity_id += 1

    return entities
