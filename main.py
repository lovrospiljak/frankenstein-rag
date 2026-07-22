"""
Application entry point.

This module launches the interactive narrative application.
It initializes the selected retrieval backend, creates the
story engine, and manages the main gameplay loop.
"""

from knowledge.graph_story import GraphStory
from rag.rag_story import RAGStory

from story.game import choose_action
from story.game import choose_scene
from story.state import GameState
from story.story_engine import StoryEngine


def choose_mode() -> str:
    """
    Allow the user to select the retrieval strategy.

    Returns:
        Selected retrieval mode.

        Possible values:
            - "rag"
            - "graph"
    """

    print("\n====================================")
    print(" Frankenstein Interactive Narrative")
    print("====================================\n")

    print("Select retrieval backend:\n")
    print("1) Vanilla RAG")
    print("2) GraphRAG")

    while True:

        choice = input("\nChoice: ").strip()

        if choice == "1":
            return "rag"

        if choice == "2":
            return "graph"

        print("Invalid selection. Please try again.")


def create_backend(mode: str):
    """
    Create the selected retrieval backend.

    Args:
        mode:
            Retrieval mode selected by the user.

    Returns:
        Initialized retrieval backend.
    """

    if mode == "rag":
        return RAGStory()

    if mode == "graph":
        return GraphStory()

    raise ValueError(f"Unknown retrieval mode: {mode}")


def main():
    """
    Run the interactive narrative application.

    Workflow:
        1. Select retrieval backend.
        2. Initialize the game state.
        3. Initialize the story engine.
        4. Select a story scene.
        5. Select a player action.
        6. Generate the next story segment.
        7. Display the generated continuation.
    """

    # ---------------------------------------------
    # Select retrieval backend
    # ---------------------------------------------

    mode = choose_mode()
    backend = create_backend(mode)

    # ---------------------------------------------
    # Initialize application
    # ---------------------------------------------

    state = GameState(
        retrieval_mode=mode,
    )

    engine = StoryEngine(
        backend=backend,
    )

    # ---------------------------------------------
    # Select story scene
    # ---------------------------------------------

    scene = choose_scene()

    state.current_scene = scene.id

    # ---------------------------------------------
    # Select player action
    # ---------------------------------------------

    action = choose_action(scene)

    # ---------------------------------------------
    # Generate the next story segment
    # ---------------------------------------------

    story = engine.generate(
        state=state,
        scene=scene,
        player_action=action,
    )

    # ---------------------------------------------
    # Display the generated story
    # ---------------------------------------------

    print("\n====================================")
    print(" Generated Story")
    print("====================================\n")

    print(story)

    print("\n====================================")


if __name__ == "__main__":
    main()
