import json
from pathlib import Path

from models.scene import Scene
from utils.caption_generator import (
    CaptionGenerator,
)


def main():

    episode_path = Path(
        "data/episodes/butterfly_episode.json"
    )

    output_path = Path(
        "output/test_captions/"
        "butterfly_episode.srt"
    )

    with open(
        episode_path,
        "r",
        encoding="utf-8",
    ) as file:

        episode_data = json.load(file)

    scenes = [
        Scene.model_validate(scene)
        for scene in episode_data["scenes"]
    ]

    durations = [
        scene.duration_seconds
        for scene in scenes
    ]

    CaptionGenerator.generate_srt(
        scenes=scenes,
        scene_durations=durations,
        output_path=output_path,
    )

    print()
    print("=" * 50)
    print("CAPTION TEST PASSED")
    print("=" * 50)
    print()
    print(
        f"SRT file: {output_path}"
    )
    print()

    with open(
        output_path,
        "r",
        encoding="utf-8",
    ) as file:

        print(file.read())


if __name__ == "__main__":
    main()