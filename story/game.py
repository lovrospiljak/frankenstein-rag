"""
Game interaction utilities.

This module contains helper functions for interacting with the
player through the terminal. It is responsible for presenting
available story scenes and player actions, but it contains no
story generation or retrieval logic.
"""

from story.scene_loader import list_scenes
from story.scenes import Scene


def choose_scene() -> Scene:
    """
    Allow the player to select the starting story scene.

    Returns:
        Scene:
            Selected story scene.
    """

    scenes = list_scenes()

    print("\nAvailable Story Scenes\n")
    print("-" * 30)

    for scene in scenes:
        print(f"{scene.id}. {scene.title}")
        print(f"   Chapter: {scene.chapter}")
        print(f"   {scene.summary}\n")

    while True:

        choice = input("Choose a scene: ").strip()

        if not choice.isdigit():
            print("Please enter a valid number.\n")
            continue

        scene_id = int(choice)

        for scene in scenes:

            if scene.id == scene_id:
                return scene

        print("Unknown scene. Please try again.\n")


def choose_action(scene: Scene) -> str:
    """
    Allow the player to choose an action for the current scene.

    Args:
        scene:
            Current story scene.

    Returns:
        str:
            Selected player action.
    """

    print(f"\nScene: {scene.title}")
    print("-" * 30)
    print(scene.summary)

    print("\nAvailable Actions:\n")

    for index, action in enumerate(scene.choices, start=1):
        print(f"{index}. {action}")

    print(f"{len(scene.choices) + 1}. Enter a custom action")

    while True:

        choice = input("\nChoose an action: ").strip()

        if not choice.isdigit():
            print("Please enter a valid number.\n")
            continue

        action_index = int(choice)

        if 1 <= action_index <= len(scene.choices):
            return scene.choices[action_index - 1]

        if action_index == len(scene.choices) + 1:

            custom = input("\nDescribe your action: ").strip()

            if custom:
                return custom

            print("Action cannot be empty.\n")
            continue

        print("Invalid selection. Please try again.\n")
