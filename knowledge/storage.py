# Standard library import
import json

# Local imports
from knowledge.entities import Entity
from knowledge.relationships import Relationship


def save_entities(entities, path):
    """Save extracted entities to a JSON file."""

    # Convert entities into dictionaries
    data = [entity.__dict__ for entity in entities]

    # Save the JSON file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_relationships(relationships, path):
    """Save extracted realationships to a JSON file."""

    # Convert relationships into dictionaries
    data = [relationships.__dict__ for relationship in relationships]

    # Save the JSON file
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_entities(path):
    """Load entities from a JSON file."""

    # Load the JSON file
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert dictionaries into Entity objects
    return [Relationship(**entity) for entity in data]


def load_relationships(path):
    """Load relationships from a JSON file."""

    # Load the JSON file
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Convert dictionaries into Relationship objects
    return [Relationship(**relationship) for relationship in data]
