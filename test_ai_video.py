from pathlib import Path

from services.ai_video_generator import (
    AIVideoGenerator,
)


def main():

    run = Path(
        "output/20260818_222639_mayas_rainbow_mystery"
    )

    image_path = (
        run
        / "images"
        / "scene_01.png"
    )

    output_path = (
        run
        / "video"
        / "scene_01_motion.mp4"
    )

    prompt = """
Maya gently looks up at the bright rainbow
with wide curious eyes and a happy surprised
expression. She slowly points toward the
rainbow with one hand. Her body moves naturally
and gently. The grass and small flowers move
slightly in a soft breeze. A few water droplets
sparkle in the air after the rain. The rainbow
remains clearly visible in the sky.

Keep Maya's appearance, clothing, proportions,
colors, facial features, and the overall
preschool 3D animation style consistent with
the input image.

Smooth natural character motion.
Gentle camera push-in.
Joyful preschool educational animation.
No text, no letters, no numbers, no logos,
no watermark.
""".strip()

    if not image_path.exists():
        raise FileNotFoundError(
            f"Scene image not found: {image_path}"
        )

    print()
    print("=" * 60)
    print("RAINBOW AI VIDEO TEST")
    print("=" * 60)
    print()
    print("Input image:")
    print(image_path)
    print()
    print("Output:")
    print(output_path)
    print()
    print(
        "Generating only 5 seconds "
        "for the first test."
    )
    print()

    generator = AIVideoGenerator(
        model="gen4_turbo"
    )

    generator.generate(
        image_path=image_path,
        output_path=output_path,
        prompt=prompt,
        duration=5,
        ratio="1280:720",
    )

    print()
    print("TEST SUCCESSFUL")
    print()
    print(
        f"Generated video: {output_path}"
    )


if __name__ == "__main__":
    main()