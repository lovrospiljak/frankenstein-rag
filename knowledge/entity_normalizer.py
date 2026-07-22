"""
Simple entity normalizer.

Normalizes spaCy entity spans into canonical strings.
"""


def normalize_entity_name(ent):
    """
    Normalize a spaCy entity.

    Parameters
    ----------
    ent : spacy.tokens.Span

    Returns
    -------
    str | None
    """

    if ent is None:
        return None

    name = ent.text.strip()

    if not name:
        return None

    # Collapse whitespace
    name = " ".join(name.split())

    # Remove surrounding punctuation
    name = name.strip(".,;:!?()[]{}\"'")

    if not name:
        return None

    return name
