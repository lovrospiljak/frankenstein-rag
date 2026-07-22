"""
Choose one canonical entity name for each cluster.
"""


def canonical_score(entity):
    """
    Score an entity name.

    Higher is better.
    """

    name = entity["name"]

    score = 0

    # Prefer multi-word names
    score += len(name.split()) * 100

    # Prefer longer names
    score += len(name)

    return score


def choose_canonical(cluster):
    """
    Choose the canonical entity.
    """

    return max(
        cluster,
        key=canonical_score,
    )
