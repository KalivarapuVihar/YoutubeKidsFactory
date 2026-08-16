import json
from pathlib import Path

from models.scene import Scene
from services.character_manager import CharacterManager


def main():

    episode_path = Path(
        "data/episodes/butterfly_episode.json"
    )

    with open(
        episode_path,
        "r",
        encoding="utf-8",
    ) as file:

        episode_data = json.load(file)

    first_scene_data = episode_data[
        "scenes"
    ][0]

    scene = Scene.model_validate(
        first_scene_data
    )

    character_manager = CharacterManager(
        Path("data/characters")
    )

    character_prompt = (
        character_manager.build_character_prompt(
            scene.characters
        )
    )

    enhanced_prompt = f"""
CHARACTER CONSISTENCY REQUIREMENTS:

{character_prompt}

SCENE:

Location:
{scene.location}

Action:
{scene.action}

Emotion:
{scene.emotion}

Camera:
{scene.camera}

Original Scene Prompt:
{scene.image_prompt}

IMPORTANT:
Keep every character visually consistent with
their character definition.

Do not redesign, rename, recolor, or replace
the characters.

Maintain consistent:
- face
- body proportions
- hairstyle
- clothing
- colors
- accessories
- species
- visual style

The scene should look like it belongs to the
same high-quality preschool animated series.

Create a polished, colorful, child-friendly
3D animated scene suitable for children ages 2-6.
"""

    print("=" * 60)
    print("CHARACTERS")
    print("=" * 60)

    print(
        scene.characters
    )

    print()

    print("=" * 60)
    print("ENHANCED IMAGE PROMPT")
    print("=" * 60)

    print(
        enhanced_prompt
    )

    print()

    print("=" * 60)
    print("TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()