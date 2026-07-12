# Standard library import
from dataclasses import dataclass


@dataclass
class Entity:
    """Represents a named entity extracted from a text."""

    id: int
    name: str
    type: str
