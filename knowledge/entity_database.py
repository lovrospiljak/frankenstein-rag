"""Build a database of every entity mention in the document.

This module extracts every named entity mentioned in the text and stores its metadata.
No entity resolution is performed here.
"""

import spacy

from knowledge.extractor import normalize_entity_name

nlp = spacy.load("en_core_web_sm")


def build_entity_database(chunks):
    """
    Build a database of entity mentions.

    Parameters
    ----------
    chunks : list[dict]

    Returns
    --------
    list[dict]
    """

    entities = []

    entity_id = 0

    for chunk in chunks:

        doc = nlp(chunk["text"])

        for ent in doc.ents:

            name = normalize_entity_name(ent)

            if not name:
                continue

            entities.append(
                {
                    "id": entity_id,
                    "name": name,
                    "label": ent.label_,
                    "chunk_id": chunk["chunk_id"],
                    "section_id": chunk["section_id"],
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                }
            )

            entity_id += 1

        return entities
