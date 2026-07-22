"""
Similarity functions used for entity resolution.
"""

from rapidfuzz import fuzz
import numpy as np

# ---------------------------------------------------------------------
# Cosine similarity
# ---------------------------------------------------------------------


def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two embedding vectors.

    Returns
    -------
    float
        Value in [0, 1].
    """

    v1 = np.asarray(vec1, dtype=np.float32)
    v2 = np.asarray(vec2, dtype=np.float32)

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = np.dot(v1, v2) / (norm1 * norm2)

    return float(similarity)


# ---------------------------------------------------------------------
# String similarity
# ---------------------------------------------------------------------


def string_similarity(name1, name2):
    """
    Compute lexical similarity between two entity names.

    Uses RapidFuzz token-based comparison.

    Returns
    -------
    float
        Value in [0,1].
    """

    score = fuzz.token_sort_ratio(
        name1.lower(),
        name2.lower(),
    )

    return score / 100.0


# ---------------------------------------------------------------------
# Type similarity
# ---------------------------------------------------------------------


def type_similarity(type1, type2):
    """
    Compare entity types.

    Returns
    -------
    float
    """

    if type1 == type2:
        return 1.0

    return 0.0


# ---------------------------------------------------------------------
# Combined similarity
# ---------------------------------------------------------------------


def combined_similarity(
    entity1,
    entity2,
    embedding_weight=0.60,
    string_weight=0.30,
    type_weight=0.10,
):
    """
    Compute combined similarity between two entities.

    Parameters
    ----------
    entity1 : dict

        {
            "name": ...,
            "type": ...,
            "embedding": [...]
        }

    entity2 : dict

    Returns
    -------
    float
    """

    emb = cosine_similarity(
        entity1["embedding"],
        entity2["embedding"],
    )

    lex = string_similarity(
        entity1["name"],
        entity2["name"],
    )

    typ = type_similarity(
        entity1["type"],
        entity2["type"],
    )

    score = embedding_weight * emb + string_weight * lex + type_weight * typ

    return score
