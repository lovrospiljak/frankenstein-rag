# Third-party imports
import spacy

# Local imports
from knowledge.relationships import Relationship
from knowledge.entity_normalizer import (
    normalize_entity_name,
)

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Entity types used to build relationships
GRAPH_ENTITY_TYPES = {
    "PERSON",
    "ORG",
    "GPE",
    "LOC",
    "FAC",
}


def extract_relationships(chunks):
    """Extract simple relationships between entities."""

    relationships = []
    seen = set()

    # Process each text chunk
    for chunk in chunks:

        doc = nlp(chunk["text"])

        # Process each sentence
        for sentence in doc.sents:

            entities = []

            verb = None

            # Collect entities and the first verb
            for token in sentence:

                if token.pos_ == "VERB" and verb is None:
                    verb = token.lemma_

            for ent in sentence.ents:

                # Ignore unsupported entity types
                if ent.label_ not in GRAPH_ENTITY_TYPES:
                    continue

                name = normalize_entity_name(ent)

                if not name:
                    continue

                entities.append(name)

            # Need at least two entities and one verb
            if len(entities) < 2:
                continue

            if verb is None:
                continue

            # Connect every pair of entities
            for i in range(len(entities)):

                for j in range(i + 1, len(entities)):

                    relationship = (
                        entities[i],
                        verb,
                        entities[j],
                    )

                    # Ignore duplicate relationships
                    if relationship in seen:
                        continue

                    seen.add(relationship)

                    relationships.append(
                        Relationship(
                            source=entities[i],
                            relation=verb,
                            target=entities[j],
                        )
                    )

    return relationships
