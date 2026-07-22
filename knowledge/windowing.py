"""
Utilities for creating overlapping chunk windows.
"""

from knowledge.entities import ChunkWindow


def build_chunk_windows(
    chunks,
    chunk_entities,
    window_size=3,
):
    """
    Build overlapping chunk windows.

    Windows never cross section boundaries.

    Parameters
    ----------
    chunks : list[dict]

    chunk_entities : list[dict]

    window_size : int

    Returns
    -------
    list[ChunkWindow]
    """

    if not chunks:
        return []

    entity_lookup = {item["chunk_id"]: item["entities"] for item in chunk_entities}

    windows = []

    n = len(chunks)

    for i in range(n):

        center_chunk = chunks[i]
        center_section = center_chunk["section_id"]

        half = window_size // 2

        start = max(0, i - half)
        end = min(n, i + half + 1)

        # keep only same section
        indices = [
            idx
            for idx in range(start, end)
            if chunks[idx]["section_id"] == center_section
        ]

        if not indices:
            continue

        window_chunks = [chunks[idx] for idx in indices]

        text = "\n\n".join(chunk["text"] for chunk in window_chunks)

        entities = sorted(
            {
                entity["name"]
                for chunk in window_chunks
                for entity in entity_lookup.get(
                    chunk["chunk_id"],
                    [],
                )
            }
        )

        windows.append(
            ChunkWindow(
                window_id=len(windows),
                center_chunk_id=center_chunk["chunk_id"],
                chunk_ids=[chunk["chunk_id"] for chunk in window_chunks],
                chunk_indices=indices,
                section_id=center_section,
                entities=entities,
            )
        )

    return windows
