"""Resolve different mentions of the same entity."""

import re


def normalize_entity(name):
    """Normalize an entity name."""

    name = name.strip()

    # Remove duplicate whitespace
    name = re.sub(r"\s", " ", name)

    return name


def resolve_entity(name):
    """Return the canonical entity name."""

    name = normalize_entity(name)

    aliases = {
        "Victor": "Victor Frankenstein",
        "Frankenstein": "Victor Frankenstein",
        "Mr. Frankenstein": "Victor Frankenstein",
        "the Creature": "Creature",
        "monster": "Creature",
        "daemon": "Creature",
        "fiend": "Creature",
        "wretch": "Creature",
    }

    return aliases.get(name, name)
