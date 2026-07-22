from collections import defaultdict

from knowledge.entities import (
    CanonicalEntity,
    EntityMention,
    ResolvedEntity,
)


def build_entity_profiles(
    resolved_entities: list[ResolvedEntity],
    mentions: list[EntityMention],
) -> list[CanonicalEntity]:
    """
    Build canonical entity profiles from resolved entities and mentions.
    """

    # original name -> canonical
    resolution = {entity.original: entity for entity in resolved_entities}

    grouped = defaultdict(list)

    for mention in mentions:

        canonical = resolution.get(mention.entity_name)

        if canonical is None:
            continue

        grouped[canonical.canonical].append(mention)

    profiles = []

    for canonical_name, group in grouped.items():

        aliases = sorted({mention.entity_name for mention in group})

        chunk_ids = sorted({mention.chunk_id for mention in group})

        section_ids = sorted({mention.section_id for mention in group})

        entity_type = group[0].entity_type

        profiles.append(
            CanonicalEntity(
                canonical=canonical_name,
                entity_type=entity_type,
                aliases=aliases,
                mention_count=len(group),
                chunk_ids=chunk_ids,
                section_ids=section_ids,
                description="",
            )
        )

    return profiles
