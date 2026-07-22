"""
Scene loading utilities.

This module provides helper functions for loading predefined
interactive story scenes from a JSON file.
"""

from __future__ import annotations

import json
from pathlib import Path

from story.scenes import Scene

SCENES_PATH = Path(__file__).parent / "scenes.json"


def load_scenes() -> list[Scene]:
    """
    Load all predefined story scenes.

    The scene definitions are stored in a JSON file and converted
    into Scene objects.

    Returns:
        list[Scene]:
            List of available story scenes.

    Raises:
        FileNotFoundError:
            If the scene definition file cannot be found.

        json.JSONDecodeError:
            If the JSON file contains invalid syntax.
    """

    with open(SCENES_PATH, encoding="utf-8") as file:
        data = json.load(file)

    return [Scene(**scene) for scene in data]


def get_scene(scene_id: int) -> Scene:
    """
    Retrieve a scene by its identifier.

    Args:
        scene_id:
            Identifier of the requested scene.

    Returns:
        Scene:
            Matching scene.

    Raises:
        ValueError:
            If no scene with the given identifier exists.
    """

    for scene in load_scenes():

        if scene.id == scene_id:
            return scene

    raise ValueError(f"Unknown scene id: {scene_id}")


def list_scenes() -> list[Scene]:
    """
    Return all available scenes.

    This function exists to make the public API explicit and allows
    future extensions such as filtering or sorting without modifying
    the calling code.

    Returns:
        list[Scene]:
            Available story scenes.
    """

    return load_scenes()
