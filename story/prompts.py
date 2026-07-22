"""
Prompt construction utilities.

This module contains helper functions for constructing prompts
used by the language model during interactive story generation.
The prompts combine retrieved context from the original novel,
previously generated story segments, the current scene, and the
player's chosen action.
"""

from story.scenes import Scene


def build_story_prompt(
    context: str,
    previous_story: str,
    scene: Scene,
    player_action: str,
) -> str:
    """
    Construct the prompt for the language model.

    The prompt contains:
        - Relevant context retrieved from the novel.
        - Previously generated story segments.
        - Current story scene.
        - Player's selected action.

    Args:
        context:
            Retrieved passages from the original novel.

        previous_story:
            Previously generated story used to preserve
            narrative continuity.

        scene:
            Current story scene.

        player_action:
            Action selected by the player.

    Returns:
        str:
            Prompt sent to the language model.
    """

    if not previous_story.strip():
        previous_story = "This is the beginning of the interactive story."

    return f"""
You are an expert novelist continuing Mary Shelley's *Frankenstein*.

Your task is to continue the story as if it were a lost chapter of the
original novel while respecting the player's decisions.

========================================================
ORIGINAL NOVEL CONTEXT
========================================================

{context}

========================================================
STORY SO FAR
========================================================

{previous_story}

========================================================
CURRENT SCENE
========================================================

Scene:
{scene.title}

Chapter:
{scene.chapter}

Description:
{scene.summary}

========================================================
PLAYER ACTION
========================================================

{player_action}

========================================================
INSTRUCTIONS
========================================================

Write the next part of the story.

Requirements:

- Remain faithful to Mary Shelley's writing style.
- Maintain consistency with previous events.
- Never contradict the retrieved novel context.
- Characters should behave consistently with their personalities.
- Use atmospheric descriptions and dialogue when appropriate.
- Treat the player's action as a natural part of the story.
- Continue the narrative instead of summarizing it.
- Do not explain your reasoning.
- Do not mention retrieval, prompts, or AI.
- Write approximately 300–500 words.

Begin the continuation immediately.
""".strip()
