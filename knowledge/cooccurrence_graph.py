from itertools import combinations

from knowledge.entities import GraphEdge


def build_cooccurrence_graph(
    windows,
    canonical_entities,
):
    """
    Build weighted co-occurrence edges.

    Parameters
    ----------
    windows : list[ChunkWindow]

    canonical_entities : list[CanonicalEntity]

    Returns
    -------
    list[GraphEdge]
    """

    # --------------------------------------------------------
    # alias -> canonical lookup
    # --------------------------------------------------------

    alias_lookup = {}

    for entity in canonical_entities:

        alias_lookup[entity.canonical] = entity.canonical

        for alias in entity.aliases:
            alias_lookup[alias] = entity.canonical

    # --------------------------------------------------------
    # Build edges
    # --------------------------------------------------------

    edge_lookup = {}

    for window in windows:

        canonical_names = []

        for entity in window.entities:

            canonical = alias_lookup.get(entity, entity)

            canonical_names.append(canonical)

        canonical_names = sorted(set(canonical_names))

        if len(canonical_names) < 2:
            continue

        for source, target in combinations(canonical_names, 2):

            key = (source, target)

            if key not in edge_lookup:

                edge_lookup[key] = GraphEdge(
                    source=source,
                    target=target,
                    weight=0,
                )

            edge = edge_lookup[key]

            edge.weight += 1

            edge.window_ids.append(window.window_id)

            edge.section_ids.append(window.section_id)

            edge.chunk_ids.extend(window.chunk_ids)

    # --------------------------------------------------------
    # Clean duplicates
    # --------------------------------------------------------

    for edge in edge_lookup.values():

        edge.window_ids = sorted(set(edge.window_ids))

        edge.section_ids = sorted(set(edge.section_ids))

        edge.chunk_ids = sorted(set(edge.chunk_ids))

    return list(edge_lookup.values())
