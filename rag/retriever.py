"""
Vector retrieval module.

This module performs semantic retrieval using a FAISS vector index.
Given a natural language query, it returns the most relevant text
chunks from the indexed novel.
"""

from dataclasses import dataclass

import faiss
import numpy as np

from rag.embeddings import embed_text


@dataclass
class RetrievedChunk:
    """
    Represents a retrieved document chunk.

    Attributes:
        chunk_id:
            Unique identifier of the retrieved chunk.

        section_id:
            Identifier of the original chapter or section.

        text:
            Retrieved text.

        score:
            Similarity score returned by the FAISS search.
    """

    chunk_id: int
    section_id: int
    text: str
    score: float


class VectorRetriever:
    """
    Dense vector retriever based on FAISS.

    The retriever converts a natural language query into an embedding,
    searches the FAISS index for the nearest neighbours, and returns
    the corresponding text chunks.
    """

    def __init__(self, index: faiss.Index, chunk_lookup: list[dict]):
        """
        Initialize the vector retriever.

        Args:
            index:
                FAISS index containing chunk embeddings.

            chunk_lookup:
                List containing metadata for every indexed chunk.
                The position of each element must correspond to the
                position of its embedding in the FAISS index.
        """

        self.index = index
        self.chunk_lookup = chunk_lookup

    def retrieve(self, query: str, k: int = 5) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant text chunks for a query.

        Args:
            query:
                Natural language search query.

            k:
                Number of chunks to retrieve.

        Returns:
            list[RetrievedChunk]:
                Retrieved chunks ordered by semantic similarity.
        """

        # Convert the query into an embedding vector.
        query_vector = embed_text(query)
        query_vector = np.array([query_vector], dtype="float32")

        # Search the FAISS index for the k nearest neighbours.
        scores, indices = self.index.search(query_vector, k)

        results: list[RetrievedChunk] = []

        # Convert FAISS search results into RetrievedChunk objects.
        for score, idx in zip(scores[0], indices[0]):

            # FAISS returns -1 when fewer than k neighbours are found.
            if idx == -1:
                continue

            chunk = self.chunk_lookup[idx]

            results.append(
                RetrievedChunk(
                    chunk_id=chunk["chunk_id"],
                    section_id=chunk["section_id"],
                    text=chunk["text"],
                    score=float(score),
                )
            )

        return results
