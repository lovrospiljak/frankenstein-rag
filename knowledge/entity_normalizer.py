# Standard library imports
import string

# Words that should not appear at the beginning of entity names
LEADING_WORDS = {
    "a",
    "an",
    "the",
}


def normalize_entity_name(ent):
    """Normalize an extracted entity name."""

    words = []

    # Keep only meaningful words
    for token in ent:

        if token.pos_ in {
            "DET",
            "PUNCT",
            "SPACE",
        }:
            continue

        words.append(token.text)

    if not words:
        return None

    name = " ".join(words).strip()

    # Remove surrounding punctuation
    name = name.strip(string.punctuation + " ")

    if not name:
        return None

    tokens = name.split()

    # Remove leading determiners
    while tokens and tokens[0].lower() in LEADING_WORDS:
        tokens.pop(0)

    if not tokens:
        return None

    return " ".join(tokens)
