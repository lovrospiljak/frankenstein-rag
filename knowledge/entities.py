from dataclasses import dataclass, field

# --------------------------------------------------
# Chunks
# --------------------------------------------------


@dataclass
class Chunk:
    chunk_id: int
    section_id: int
    text: str


@dataclass
class ChunkWindow:
    window_id: int
    center_chunk_id: int
    chunk_ids: list[int]
    chunk_indices: list[int]
    section_id: int
    entities: list[str]


# --------------------------------------------------
# Entities
# --------------------------------------------------


@dataclass
class Entity:
    id: int
    name: str
    type: str


@dataclass
class EntityMention:
    chunk_id: int
    section_id: int
    entity_name: str
    entity_type: str
    start: int
    end: int
    text: str


@dataclass
class ResolvedEntity:
    """
    Output of local LLM entity normalization.
    """

    original: str
    canonical: str
    entity_type: str


@dataclass
class CanonicalEntity:
    """
    Final canonical entity after clustering/entity resolution.
    """

    canonical: str
    entity_type: str

    aliases: list[str] = field(default_factory=list)

    description: str = ""

    mention_count: int = 0

    chunk_ids: list[int] = field(default_factory=list)

    section_ids: list[int] = field(default_factory=list)


# --------------------------------------------------
# Relationships
# --------------------------------------------------


@dataclass
class Relationship:
    source: str
    relation: str
    target: str

    window_id: int = -1
    section_id: int = -1
    chunk_ids: list[int] = field(default_factory=list)

    evidence: str = ""


# --------------------------------------------------
# LLM Extraction
# --------------------------------------------------


@dataclass
class ExtractionResult:
    entities: list[ResolvedEntity] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)


@dataclass
class GraphEdge:
    """
    Weighted co-occurrence edge between two canonical entities.
    """

    source: str
    target: str

    weight: int = 0

    chunk_ids: list[int] = field(default_factory=list)

    section_ids: list[int] = field(default_factory=list)

    window_ids: list[int] = field(default_factory=list)
