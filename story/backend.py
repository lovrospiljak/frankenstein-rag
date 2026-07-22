"""
Story retrieval backend interface.

This module defines the abstract interface implemented by all
story retrieval backends. The StoryEngine depends only on this
interface, allowing different retrieval strategies to be used
without modifying the story generation pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class StoryBackend(ABC):
    """
    Abstract base class for story retrieval backends.

    A retrieval backend is responsible for locating passages from the
    source novel that are relevant to the current narrative state.
    Implementations may use different retrieval strategies, such as
    dense vector search or knowledge graph traversal.

    The StoryEngine communicates exclusively through this interface,
    making the retrieval implementation interchangeable.
    """

    @abstractmethod
    def retrieve(self, query: str) -> str:
        """
        Retrieve story context relevant to a query.

        Args:
            query:
                Natural language description of the current story
                situation or narrative event.

        Returns:
            str:
                Retrieved context that will be incorporated into the
                language model prompt.
        """

        raise NotImplementedError
