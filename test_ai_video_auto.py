import json
from pathlib import Path

from models.storyboard import Storyboard
from services.ai_motion_prompt_generator import (
    AIMotionPromptGenerator,
)
from services.ai_video_generator import AIVideoGenerator


def main():

    run = Path(
        "output/20260818_222639_mayas_rainbow_mystery"
    )

    storyboard_path = run / "storyboard.json"

    image_path = (
        run
        / "images"
        / "scene_01.png"
    )

    output_path = (
        run
        / "video"
        / "scene_01_motion_auto.mp4"
    )

    print()
    print("=" * 60)
    print("AUTOMATED AI VIDEO TEST")
    print("=" * 60)
    print()

    if not storyboard_path.exists():
        raise FileNotFoundError(
            f"Storyboard not found: {storyboard_path}"
        )

    if not image_path.exists():
        raise FileNotFoundError(
            f"Scene image not found: {image_path}"
        )

    storyboard = Storyboard.model_validate(
        json.loads(
            storyboard_path.read_text(
                encoding="utf-8"
            )
        )
    )

    scene = storyboard.scenes[0]

    print(
        f"Scene: {scene.scene_number}"
    )
    print(
        f"Image: {image_path}"
    )
    print(
        f"Output: {output_path}"
    )
    print()

    # Generate the Runway motion prompt locally.
    # This does NOT use OpenAI and does NOT cost credits.
    motion_prompt = (
        AIMotionPromptGenerator.generate(
            scene
        )
    )

    print("=" * 60)
    print("GENERATED MOTION PROMPT")
    print("=" * 60)
    print()
    print(motion_prompt)
    print()

    print("=" * 60)
    print("STARTING RUNWAY TEST")
    print("=" * 60)
    print()
    print(
        "Generating ONLY Scene 1 for 5 seconds."
    )
    print(
        "This will consume Runway credits."
    )
    print()

    generator = AIVideoGenerator(
        model="gen4_turbo"
    )

    generator.generate(
        image_path=image_path,
        output_path=output_path,
        prompt=motion_prompt,
        duration=5,
        ratio="1280:720",
    )

    print()
    print("=" * 60)
    print("AUTOMATED TEST SUCCESSFUL")
    print("=" * 60)
    print()
    print(
        f"Generated video: {output_path}"
    )
    print()


if __name__ == "__main__":
    main()