"""
Story scene definitions.

This module defines the data structures used to represent
predefined interactive story scenes.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Scene:
    """
    Represents a predefined branching point in the story.

    Attributes:
        id:
            Unique scene identifier.

        title:
            Human-readable scene title.

        chapter:
            Source chapter in the original novel.

        summary:
            Short description displayed to the player.

        query:
            Retrieval query used to obtain relevant context.

        choices:
            Available player actions.
    """

    id: int
    title: str
    chapter: int
    summary: str
    query: str
    choices: list[str]
