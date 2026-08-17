from pathlib import Path

from models.scene import Scene
from utils.caption_generator import (
    CaptionGenerator,
)


def main():

    scenes = [
        Scene(
            scene_number=1,
            narration="Butterflies are amazing!",
            image_prompt="Butterfly garden scene.",
            duration_seconds=4,
            caption_text="Butterflies are amazing!",
            location="Butterfly garden",
            characters=["Maya"],
            action="Maya discovers a beautiful butterfly.",
            emotion="Excited",
            camera="Wide shot",
        ),
        Scene(
            scene_number=2,
            narration="Look at those beautiful wings!",
            image_prompt="Butterfly garden scene.",
            duration_seconds=5,
            caption_text="Look at those beautiful wings!",
            location="Butterfly garden",
            characters=["Maya"],
            action="Maya watches the butterfly.",
            emotion="Delighted",
            camera="Medium shot",
        ),
        Scene(
            scene_number=3,
            narration="Butterflies begin their lives as tiny eggs.",
            image_prompt="Butterfly garden scene.",
            duration_seconds=3,
            caption_text="Butterflies begin their lives as tiny eggs.",
            location="Garden",
            characters=["Maya"],
            action="Maya learns about butterfly eggs.",
            emotion="Curious",
            camera="Close-up",
        ),
        Scene(
            scene_number=4,
            narration="Then a caterpillar hatches.",
            image_prompt="Butterfly garden scene.",
            duration_seconds=4,
            caption_text="Then a caterpillar hatches.",
            location="Garden",
            characters=["Maya"],
            action="A caterpillar appears.",
            emotion="Surprised",
            camera="Close-up",
        ),
        Scene(
            scene_number=5,
            narration="The caterpillar eats and grows.",
            image_prompt="Butterfly garden scene.",
            duration_seconds=4,
            caption_text="The caterpillar eats and grows.",
            location="Garden",
            characters=["Maya"],
            action="The caterpillar munches on leaves.",
            emotion="Happy",
            camera="Medium shot",
        ),
        Scene(
            scene_number=6,
            narration="Next comes the chrysalis.",
            image_prompt="Butterfly garden scene.",
            duration_seconds=5,
            caption_text="Next comes the chrysalis.",
            location="Garden",
            characters=["Maya"],
            action="Maya observes a chrysalis.",
            emotion="Curious",
            camera="Close-up",
        ),
        Scene(
            scene_number=7,
            narration="Inside, an amazing transformation happens!",
            image_prompt="Butterfly garden scene.",
            duration_seconds=5,
            caption_text="Inside, an amazing transformation happens!",
            location="Garden",
            characters=["Maya"],
            action="The chrysalis transforms.",
            emotion="Amazed",
            camera="Close-up",
        ),
        Scene(
            scene_number=8,
            narration="And finally, a beautiful butterfly emerges.",
            image_prompt="Butterfly garden scene.",
            duration_seconds=5,
            caption_text="And finally, a beautiful butterfly emerges.",
            location="Garden",
            characters=["Maya"],
            action="The butterfly emerges.",
            emotion="Excited",
            camera="Wide shot",
        ),
        Scene(
            scene_number=9,
            narration="Egg, caterpillar, chrysalis, butterfly!",
            image_prompt="Butterfly garden scene.",
            duration_seconds=6,
            caption_text="Egg, caterpillar, chrysalis, butterfly!",
            location="Wonderland Valley",
            characters=["Maya"],
            action="Maya celebrates the life cycle.",
            emotion="Joyful",
            camera="Wide shot",
        ),
        Scene(
            scene_number=10,
            narration="What a wonderful butterfly adventure!",
            image_prompt="Butterfly garden scene.",
            duration_seconds=4,
            caption_text="What a wonderful butterfly adventure!",
            location="Wonderland Valley",
            characters=["Maya"],
            action="Maya waves goodbye.",
            emotion="Happy",
            camera="Wide shot",
        ),
    ]

    actual_durations = [
        3.648,
        5.352,
        3.408,
        3.912,
        3.960,
        4.920,
        4.608,
        4.656,
        6.216,
        3.600,
    ]

    output_path = Path(
        "output/"
        "20260810_084916_butterflies/"
        "butterfly_test.srt"
    )

    CaptionGenerator.generate_srt(
        scenes=scenes,
        scene_durations=actual_durations,
        output_path=output_path,
    )

    print()
    print("=" * 60)
    print("MATCHING SRT CREATED")
    print("=" * 60)
    print()
    print(
        f"SRT: {output_path}"
    )


if __name__ == "__main__":
    main()