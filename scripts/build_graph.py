"""
Build the GraphRAG knowledge graph.

Pipeline

canonical_entities
        +
chunks
        ↓
extract chunk entities
        ↓
build chunk windows
        ↓
build co-occurrence edges
        ↓
NetworkX graph
"""

from knowledge.storage import load_json, save_json

from knowledge.extractor import extract_chunk_entities

from knowledge.windowing import build_chunk_windows

from knowledge.cooccurrence_graph import build_cooccurrence_graph

from knowledge.graph_builder import build_graph

from knowledge.storage import (
    load_json,
    save_json,
    save_graph,
)

from knowledge.entities import CanonicalEntity

# -----------------------------------------------------

CHUNKS_PATH = "data/processed/chunks.json"

CANONICAL_PATH = "data/processed/canonical_entities.json"

GRAPH_PATH = "data/processed/knowledge_graph.graphml"

WINDOWS_PATH = "data/processed/windows.json"

# -----------------------------------------------------


def main():

    print("Loading chunks...")

    chunks = load_json(
        CHUNKS_PATH,
    )

    print(f"{len(chunks)} chunks")

    print()

    print("Loading canonical entities...")

    canonical_entities = [
        CanonicalEntity(**entity)
        for entity in load_json(
            CANONICAL_PATH,
        )
    ]

    print(f"{len(canonical_entities)} canonical entities")

    print()

    print("Extracting entities from chunks...")

    chunk_entities = extract_chunk_entities(
        chunks,
    )

    print(f"{len(chunk_entities)} chunks with entities")

    print()

    print("Building windows...")

    windows = build_chunk_windows(
        chunks,
        chunk_entities,
        window_size=3,
    )

    print(f"{len(windows)} windows")

    print("Saving windows...")

    save_json(
        [window.__dict__ for window in windows],
        WINDOWS_PATH,
    )

    print()

    print("Building co-occurrence graph...")

    edges = build_cooccurrence_graph(
        windows,
        canonical_entities,
    )

    print(f"{len(edges)} graph edges")

    print()

    print("Creating NetworkX graph...")

    graph = build_graph(
        canonical_entities,
        edges,
    )

    print()

    print("Saving graph...")

    save_graph(
        graph,
        GRAPH_PATH,
    )

    print()

    print("Done.")
    print(f"Nodes : {graph.number_of_nodes()}")
    print(f"Edges : {graph.number_of_edges()}")


if __name__ == "__main__":
    main()
