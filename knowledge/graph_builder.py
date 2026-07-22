import networkx as nx

from knowledge.entities import (
    CanonicalEntity,
    GraphEdge,
)


def build_graph(
    entities: list[CanonicalEntity],
    edges: list[GraphEdge],
) -> nx.Graph:

    graph = nx.Graph()

    for entity in entities:

        graph.add_node(
            entity.canonical,
            entity_type=entity.entity_type,
            aliases=entity.aliases,
            description=entity.description,
            mention_count=entity.mention_count,
            chunk_ids=entity.chunk_ids,
            section_ids=entity.section_ids,
        )

    for edge in edges:

        graph.add_edge(
            edge.source,
            edge.target,
            weight=edge.weight,
            window_ids=edge.window_ids,
        )

    return graph
