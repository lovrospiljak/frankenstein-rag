"""
Graph-based retrieval.

This module retrieves relevant narrative windows using a knowledge graph.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

import networkx as nx

from knowledge.entity_faiss import search_entities
from rag.embeddings import embed_text


@dataclass(slots=True)
class GraphRetrieval:
    """
    Result of a graph retrieval operation.

    Attributes:
        seed_entities:
            Entities detected in the user query.

        nodes:
            Expanded graph neighborhood.

        window_ids:
            Ranked narrative windows.
    """

    seed_entities: list[str]
    nodes: list[str]
    window_ids: list[int]


class GraphRetriever:
    """
    Graph-based retrieval over the story knowledge graph.
    """

    def __init__(
        self,
        graph: nx.Graph,
        entity_index=None,
        entity_lookup=None,
    ):
        """
        Initialize the graph retriever.

        Args:
            graph:
                Story knowledge graph.

            entity_index:
                FAISS entity index.

            entity_lookup:
                Entity lookup table.
        """

        self.graph = graph
        self.entity_index = entity_index
        self.entity_lookup = entity_lookup

        #
        # alias -> canonical entity
        #

        self.alias_lookup: dict[str, str] = {}

        for node, data in self.graph.nodes(data=True):

            self.alias_lookup[node.casefold()] = node

            for alias in data.get("aliases", []):

                self.alias_lookup[alias.casefold()] = node

        #
        # entity -> {window_id: score}
        #

        self.entity_windows = defaultdict(lambda: defaultdict(int))

        for u, v, data in self.graph.edges(data=True):

            weight = data.get("weight", 1)

            for window in data.get("window_ids", []):

                self.entity_windows[u][window] += weight
                self.entity_windows[v][window] += weight

    # ============================================================
    # Entity detection
    # ============================================================

    def find_seed_entities_exact(
        self,
        query: str,
    ) -> set[str]:
        """
        Find entities using exact alias matching.
        """

        query = query.casefold()

        matches = set()

        for alias, canonical in self.alias_lookup.items():

            if re.search(
                rf"\b{re.escape(alias)}\b",
                query,
            ):
                matches.add(canonical)

        return matches

    def find_seed_entities_semantic(
        self,
        query: str,
        k: int = 5,
        threshold: float = 0.55,
    ) -> set[str]:
        """
        Find entities using semantic similarity.
        """

        if self.entity_index is None:

            return set()

        embedding = embed_text(query)

        results = search_entities(
            query_embedding=embedding,
            index=self.entity_index,
            lookup=self.entity_lookup,
            k=k,
        )

        return {entity["name"] for entity in results if entity["score"] >= threshold}

    def find_seed_entities(
        self,
        query: str,
    ) -> list[str]:
        """
        Detect seed entities.

        Exact matching is preferred. Semantic search is used only if
        no exact entity is found.
        """

        exact = self.find_seed_entities_exact(query)

        if exact:

            return sorted(exact)

        semantic = self.find_seed_entities_semantic(query)

        return sorted(semantic)

    # ============================================================
    # Graph expansion
    # ============================================================

    def expand(
        self,
        seed_nodes: list[str],
        max_neighbors: int = 10,
    ) -> set[str]:
        """
        Expand the graph around seed entities.
        """

        visited = set(seed_nodes)

        for node in seed_nodes:

            if node not in self.graph:
                continue

            neighbors = sorted(
                self.graph[node].items(),
                key=lambda item: item[1].get("weight", 0),
                reverse=True,
            )

            for neighbor, _ in neighbors[:max_neighbors]:

                visited.add(neighbor)

        return visited

    # ============================================================
    # Window ranking
    # ============================================================

    def rank_windows(
        self,
        nodes: set[str],
        seed_nodes: list[str],
        max_windows: int = 10,
    ) -> list[int]:
        """
        Rank narrative windows.
        """

        scores = defaultdict(int)

        for node in nodes:

            for window, weight in self.entity_windows.get(
                node,
                {},
            ).items():

                scores[window] += weight

                #
                # Boost windows containing the original seed entity.
                #

                if node in seed_nodes:

                    scores[window] += 10

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [window for window, _ in ranked[:max_windows]]

    # ============================================================
    # Public API
    # ============================================================

    def retrieve(
        self,
        query: str,
        max_neighbors: int = 10,
        max_windows: int = 10,
    ) -> GraphRetrieval:
        """
        Retrieve relevant narrative windows.

        Args:
            query:
                User query.

            max_neighbors:
                Number of graph neighbors explored.

            max_windows:
                Number of returned windows.

        Returns:
            Graph retrieval result.
        """

        seeds = self.find_seed_entities(query)

        if not seeds:

            return GraphRetrieval(
                seed_entities=[],
                nodes=[],
                window_ids=[],
            )

        #
        # Single entity:
        # don't expand
        #

        if len(seeds) == 1:

            nodes = set(seeds)

        else:

            nodes = self.expand(
                seeds,
                max_neighbors=max_neighbors,
            )

        windows = self.rank_windows(
            nodes,
            seeds,
            max_windows=max_windows,
        )

        return GraphRetrieval(
            seed_entities=sorted(seeds),
            nodes=sorted(nodes),
            window_ids=windows,
        )
