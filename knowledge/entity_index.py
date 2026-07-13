# Standard library imports
from collections import defaultdict

# Words that should not be indexed individually
IGNORED_TOKENS = {
    "a",
    "an",
    "and",
    "at",
    "for",
    "from",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


def build_entity_index(graph):
    """Build a lookup index for graph entities."""

    index = defaultdict(list)

    # Process graph nodes
    for node, data in graph.nodes(data=True):

        # Ignore chunk nodes
        if data["node_type"] != "entity":
            continue

        name = node.lower()

        # Index the complete entity name
        index[name].append(node)

        tokens = name.split()

        # Index individual words
        for token in tokens:

            # Ignore common words
            if token in IGNORED_TOKENS:
                continue

            index[token].append(node)

        # Index progressive phrases
        #
        # Example:
        # "Victor Frankenstein"
        #   -> "Victor Frankenstein"
        #
        # "University of Ingolstadt"
        #   -> "University of"
        #   -> "University of Ingolstadt"
        #
        for i in range(2, len(tokens) + 1):

            phrase = " ".join(tokens[:i])

            index[phrase].append(node)

    return dict(index)
