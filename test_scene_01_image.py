import json
from pathlib import Path

from models.scene import Scene
from services.openai_service import OpenAIService
from services.character_manager import CharacterManager
from services.image_generator import ImageGenerator


def main():

    episode_path = Path(
        "data/episodes/butterfly_episode.json"
    )

    output_path = Path(
        "output/test_scene_01/"
        "scene_01_maya_butterfly.png"
    )

    with open(
        episode_path,
        "r",
        encoding="utf-8",
    ) as file:

        episode_data = json.load(file)

    scene_data = (
        episode_data["scenes"][0]
    )

    scene = Scene.model_validate(
        scene_data
    )

    character_manager = CharacterManager(
        Path("data/characters")
    )

    ai_service = OpenAIService()

    image_generator = ImageGenerator(
        ai_service,
        character_manager,
    )

    print()
    print("=" * 60)
    print("GENERATING PRODUCTION TEST")
    print("=" * 60)
    print()
    print(f"Scene: {scene.scene_number}")
    print(f"Characters: {scene.characters}")
    print(f"Location: {scene.location}")
    print()

    print("Character references:")

    for character in scene.characters:

        reference_path = (
            character_manager.get_reference_image(
                character
            )
        )

        print(
            f"  {character}: "
            f"{reference_path}"
        )

    print()
    print("Sending request to gpt-image-1...")
    print()

    image_generator.generate(
        scene=scene,
        output_path=output_path,
    )

    print()
    print("=" * 60)
    print("PRODUCTION TEST COMPLETED")
    print("=" * 60)
    print()
    print(
        f"Image: {output_path}"
    )


if __name__ == "__main__":
    main()