"""
Vanilla Retrieval-Augmented Generation backend.

This module implements the StoryBackend interface using semantic
vector retrieval. Relevant passages are retrieved from a FAISS index
and returned as contextual information for story generation.
"""

from __future__ import annotations

import json
from pathlib import Path

import faiss

from rag.retriever import VectorRetriever
from story.backend import StoryBackend


class RAGStory(StoryBackend):
    """
    Vanilla Retrieval-Augmented Generation backend.

    This backend loads the FAISS index and chunk metadata during
    initialization and performs semantic retrieval for each player
    interaction.

    Attributes:
        retriever:
            Vector retriever responsible for semantic search.
    """

    def __init__(
        self,
        index_path: str = "data/processed/faiss.index",
        chunks_path: str = "data/processed/chunks.json",
        k: int = 5,
    ):
        """
        Initialize the RAG backend.

        Args:
            index_path:
                Path to the FAISS index.

            chunks_path:
                Path to the indexed chunk metadata.

            k:
                Default number of chunks retrieved for each query.

        Raises:
            FileNotFoundError:
                If one of the required files cannot be found.
        """

        self.k = k

        index_file = Path(index_path)
        chunks_file = Path(chunks_path)

        if not index_file.exists():
            raise FileNotFoundError(f"FAISS index not found: {index_file}")

        if not chunks_file.exists():
            raise FileNotFoundError(f"Chunk metadata not found: {chunks_file}")

        # Load the FAISS vector index.
        index = faiss.read_index(str(index_file))

        # Load chunk metadata.
        with open(chunks_file, encoding="utf-8") as file:
            chunk_lookup = json.load(file)

        self.retriever = VectorRetriever(
            index=index,
            chunk_lookup=chunk_lookup,
        )

    def retrieve(self, query: str) -> str:
        """
        Retrieve story context for a narrative event.

        Args:
            query:
                Natural language description of the current story
                situation.

        Returns:
            str:
                Retrieved story context ready for prompt
                construction.
        """

        chunks = self.retriever.retrieve(
            query=query,
            k=self.k,
        )

        return "\n\n".join(chunk.text for chunk in chunks)

    def retrieve_chunks(self, query: str):
        """
        Retrieve structured chunk objects.

        This helper is primarily intended for debugging and
        evaluation.

        Args:
            query:
                Natural language retrieval query.

        Returns:
            list[RetrievedChunk]:
                Retrieved chunk objects.
        """

        return self.retriever.retrieve(
            query=query,
            k=self.k,
        )
