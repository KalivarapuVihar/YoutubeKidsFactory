import json
import shutil
from pathlib import Path

from models.storyboard import Storyboard
from services.ai_motion_prompt_generator import (
    AIMotionPromptGenerator,
)
from services.ai_video_generator import AIVideoGenerator


RUN = Path(
    "output/20260818_222639_mayas_rainbow_mystery"
)

DURATION = 5
RATIO = "1280:720"


def main():

    storyboard_path = RUN / "storyboard.json"
    images_dir = RUN / "images"
    video_dir = RUN / "video"

    print()
    print("=" * 70)
    print("YOUTUBE KIDS FACTORY - AI MOTION GENERATION")
    print("=" * 70)
    print()

    if not storyboard_path.exists():
        raise FileNotFoundError(
            f"Storyboard not found: {storyboard_path}"
        )

    if not images_dir.exists():
        raise FileNotFoundError(
            f"Images directory not found: {images_dir}"
        )

    video_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    storyboard = Storyboard.model_validate(
        json.loads(
            storyboard_path.read_text(
                encoding="utf-8"
            )
        )
    )

    print(
        f"Run: {RUN}"
    )
    print(
        f"Scenes: {len(storyboard.scenes)}"
    )
    print(
        f"AI motion duration: {DURATION} seconds"
    )
    print(
        f"Ratio: {RATIO}"
    )
    print()

    generator = AIVideoGenerator(
        model="gen4_turbo"
    )

    generated = 0
    skipped = 0

    for scene in storyboard.scenes:

        scene_number = scene.scene_number

        image_path = (
            images_dir
            / f"scene_{scene_number:02d}.png"
        )

        final_motion_path = (
            video_dir
            / f"scene_{scene_number:02d}_motion.mp4"
        )

        auto_motion_path = (
            video_dir
            / f"scene_{scene_number:02d}_motion_auto.mp4"
        )

        print()
        print("=" * 70)
        print(
            f"SCENE {scene_number} / "
            f"{len(storyboard.scenes)}"
        )
        print("=" * 70)
        print()

        if final_motion_path.exists():

            print(
                "Existing motion video found."
            )
            print(
                f"Skipping: {final_motion_path}"
            )

            skipped += 1
            continue

        # Scene 1 was already successfully tested
        # using the automated motion pipeline.
        #
        # Reuse it instead of spending Runway credits again.
        if auto_motion_path.exists():

            print(
                "Existing automated motion video found."
            )
            print(
                "Reusing it without generating again."
            )

            shutil.copy2(
                auto_motion_path,
                final_motion_path,
            )

            print(
                f"Saved: {final_motion_path}"
            )

            skipped += 1
            continue

        if not image_path.exists():

            raise FileNotFoundError(
                f"Scene image not found: {image_path}"
            )

        prompt = (
            AIMotionPromptGenerator.generate(
                scene
            )
        )

        print(
            f"Motion prompt length: {len(prompt)}"
        )

        if len(prompt) > 1000:

            raise ValueError(
                f"Scene {scene_number} motion "
                f"prompt is too long: "
                f"{len(prompt)} characters"
            )

        print(
            f"Generating {DURATION}-second "
            "Runway video..."
        )
        print(
            "This scene will consume credits."
        )
        print()

        generator.generate(
            image_path=image_path,
            output_path=final_motion_path,
            prompt=prompt,
            duration=DURATION,
            ratio=RATIO,
        )

        generated += 1

        print()
        print(
            f"Scene {scene_number} completed."
        )
        print(
            f"Output: {final_motion_path}"
        )

    print()
    print("=" * 70)
    print("AI MOTION GENERATION COMPLETE")
    print("=" * 70)
    print()
    print(
        f"New videos generated: {generated}"
    )
    print(
        f"Existing videos reused/skipped: {skipped}"
    )
    print(
        f"Total scenes: {len(storyboard.scenes)}"
    )
    print()
    print("Motion videos:")
    print()

    for scene in storyboard.scenes:

        path = (
            video_dir
            / f"scene_{scene.scene_number:02d}_motion.mp4"
        )

        if path.exists():
            print(f"  OK  {path}")
        else:
            print(f"  MISSING  {path}")

    print()


if __name__ == "__main__":
    main()