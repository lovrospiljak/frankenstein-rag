"""
Build rich profiles for every entity.
"""

from collections import defaultdict


def build_entity_profiles(
    chunks,
    chunk_entities,
    entities,
    max_chunks=5,
):
    """
    Build contextual profiles for entities.
    """

    chunk_lookup = {chunk["chunk_id"]: chunk for chunk in chunks}

    entity_info = defaultdict(
        lambda: {
            "count": 0,
            "sections": set(),
            "chunk_ids": [],
        }
    )

    # --------------------------------------------------------

    for chunk in chunk_entities:

        chunk_id = chunk["chunk_id"]

        section_id = chunk_lookup[chunk_id]["section_id"]

        for entity in chunk["entities"]:

            info = entity_info[entity["name"]]

            info["count"] += 1

            info["sections"].add(section_id)

            info["chunk_ids"].append(chunk_id)

    # --------------------------------------------------------

    profiles = []

    for entity in entities:

        info = entity_info[entity["name"]]

        unique_chunks = sorted(set(info["chunk_ids"]))[:max_chunks]

        contexts = []

        for chunk_id in unique_chunks:

            contexts.append(chunk_lookup[chunk_id]["text"])

        profile = {
            "id": entity["id"],
            "name": entity["name"],
            "type": entity["type"],
            "mention_count": info["count"],
            "sections": sorted(info["sections"]),
            "chunk_ids": unique_chunks,
            "profile": (
                f"Entity: {entity['name']}\n"
                f"Type: {entity['type']}\n"
                f"Mention count: {info['count']}\n"
                f"Sections: "
                f"{', '.join(map(str, sorted(info['sections'])))}\n\n"
                f"Representative contexts:\n\n" + "\n\n".join(contexts)
            ),
        }

        profiles.append(profile)

    return profiles
