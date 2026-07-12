# Standard library import
from dataclasses import dataclass


@dataclass
class Relationship:
    """Represents a relationship between two entities."""

    source: int
    relation: str
    target: int
