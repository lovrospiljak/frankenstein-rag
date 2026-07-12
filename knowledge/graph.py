# Standard library imports
from dataclasses import dataclass, field

# Local imports
from knowledge.entities import Entity
from knowledge.relationships import Relationship


@dataclass
class KnowledgeGraph:
    """Represents the knowledge graph extracted from a document."""

    # Extracted entities
    entities: list[Entity] = field(default_factory=list)

    # Relationships between entities
    relationships: list[Relationship] = field(default_factory=list)
