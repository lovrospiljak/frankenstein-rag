"""
Story generation engine.

The StoryEngine coordinates the interactive storytelling pipeline.
It retrieves relevant context from the selected retrieval backend,
constructs a prompt for the language model, generates the next
story continuation, and updates the game state.

The engine is independent of the underlying retrieval strategy.
Any backend implementing the StoryBackend interface can be used.
"""

from llm.local import generate

from story.backend import StoryBackend
from story.prompts import build_story_prompt
from story.scenes import Scene
from story.state import GameState


class StoryEngine:
    """
    Coordinates the interactive narrative generation pipeline.

    The StoryEngine orchestrates the interaction between the
    retrieval backend, prompt construction, language model,
    and game state.
    """

    def __init__(self, backend: StoryBackend):
        """
        Initialize the story engine.

        Args:
            backend:
                Retrieval backend used to obtain story context.
        """

        self.backend = backend

    def generate(
        self,
        state: GameState,
        scene: Scene,
        player_action: str,
    ) -> str:
        """
        Generate the next segment of the interactive story.

        Workflow:
            1. Retrieve relevant story context.
            2. Gather previously generated narrative.
            3. Construct the language model prompt.
            4. Generate the continuation.
            5. Update the game state.

        Args:
            state:
                Current game state.

            scene:
                Current story scene.

            player_action:
                Action selected by the player.

        Returns:
            Generated story continuation.
        """

        # Retrieve relevant context from the selected backend.
        context = self.backend.retrieve(scene.query)

        # Include recent story history to preserve narrative continuity.
        previous_story = "\n\n".join(state.generated_story[-3:])

        # Construct the language model prompt.
        prompt = build_story_prompt(
            context=context,
            previous_story=previous_story,
            scene=scene,
            player_action=player_action,
        )

        # Generate the continuation.
        story = generate(
            prompt=prompt,
            temperature=0.7,
            num_predict=768,
            think=False,
        )

        # Record the player's decision.
        state.history.append(
            {
                "turn": state.turn + 1,
                "scene_id": scene.id,
                "scene": scene.title,
                "action": player_action,
            }
        )

        # Store the generated continuation.
        state.generated_story.append(story)

        # Advance the game state.
        state.turn += 1
        state.current_scene = scene.id

        return story

    def get_story(self, state: GameState) -> str:
        """
        Return the complete generated story.

        Args:
            state:
                Current game state.

        Returns:
            Complete generated narrative.
        """

        return "\n\n".join(state.generated_story)

    def reset(self, state: GameState) -> None:
        """
        Reset the game state.

        Args:
            state:
                State to reset.
        """

        state.current_scene = None
        state.turn = 0
        state.history.clear()
        state.generated_story.clear()
        state.finished = False
