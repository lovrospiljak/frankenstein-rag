# Third-party imports
import spacy

from knowledge.entity_normalizer import normalize_entity_name

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Question words that should not be used as query terms
QUESTION_WORDS = {
    "who",
    "what",
    "where",
    "when",
    "why",
    "which",
    "whose",
    "whom",
    "how",
}

# Generic words that add little retrieval value
STOP_WORDS = {
    "thing",
    "someone",
    "somebody",
    "something",
    "anything",
    "everything",
    "nothing",
}


def extract_query_terms(question):
    """Extract important terms from a question."""

    doc = nlp(question)

    terms = []
    seen = set()

    # Add a query term if it has not been added before
    def add_term(term):

        term = term.strip()

        if not term:
            return

        key = term.lower()

        if key in seen:
            return

        seen.add(key)

        terms.append(term)

    # Extract named entities
    for ent in doc.ents:

        name = normalize_entity_name(ent)

        if name is None:
            continue

        add_term(name)

    # Extract noun chunks
    for chunk in doc.noun_chunks:

        root = chunk.root.lemma_.lower()

        # Ignore question words
        if root in QUESTION_WORDS:
            continue

        # Ignore generic words
        if root in STOP_WORDS:
            continue

        name = normalize_entity_name(chunk)

        if name is None:
            continue

        add_term(name)

    # Extract important nouns
    for token in doc:

        # Keep only nouns and proper nouns
        if token.pos_ not in {
            "NOUN",
            "PROPN",
        }:
            continue

        term = token.lemma_.strip()

        if not term:
            continue

        key = term.lower()

        # Ignore question words
        if key in QUESTION_WORDS:
            continue

        # Ignore generic words
        if key in STOP_WORDS:
            continue

        add_term(term)

    return terms
