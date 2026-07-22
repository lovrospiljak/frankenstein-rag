"""
Graph Retrieval-Augmented Generation backend.
"""

from __future__ import annotations

import pickle
from pathlib import Path

import faiss
import networkx as nx
import json

from knowledge.graph_retriever import GraphRetriever
from knowledge.window_repository import WindowRepository
from story.backend import StoryBackend


class GraphStory(StoryBackend):
    """
    Story backend powered by a knowledge graph.
    """

    def __init__(
        self,
        graph_path: str = "data/processed/knowledge_graph.pkl",
        entity_index_path: str = "data/processed/entity.index",
        entity_lookup_path: str = "data/processed/entity_lookup.json",
        windows_path: str = "data/processed/windows.json",
    ):
        graph_file = Path(graph_path)

        if not graph_file.exists():
            raise FileNotFoundError(f"Graph not found: {graph_file}")

        # Load the graph.
        with open(graph_file, "rb") as file:
            graph = pickle.load(file)

        # Load the entity lookup.
        with open(entity_lookup_path, encoding="utf-8") as file:
            entity_lookup = json.load(file)

        # Load the FAISS index.
        entity_index = None
        if Path(entity_index_path).exists():
            entity_index = faiss.read_index(entity_index_path)

        self.retriever = GraphRetriever(
            graph=graph,
            entity_index=entity_index,
            entity_lookup=entity_lookup,
        )

        self.windows = WindowRepository(windows_path)

    def retrieve(
        self,
        query: str,
    ) -> str:
        """
        Retrieve graph context.
        """

        result = self.retriever.retrieve(query)

        texts = self.windows.get_texts(
            result.window_ids,
        )

        return "\n\n".join(texts)
