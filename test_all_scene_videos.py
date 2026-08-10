import json
from pathlib import Path

from services.video_renderer import VideoRenderer
from models.storyboard import Storyboard

def main():

    storyboard_files = sorted(
        Path("output").glob(
            "*/storyboard.json"
        )
    )

    if not storyboard_files:
        raise FileNotFoundError(
            "No storyboard.json found."
        )

    storyboard_path = storyboard_files[-1]

    run_directory = (
        storyboard_path.parent
    )

    with open(
    storyboard_path,
    "r",
    encoding="utf-8",
    ) as file:

        storyboard_data = json.load(file)

    storyboard = Storyboard.model_validate(
        storyboard_data
    )

    video_paths = (
        VideoRenderer.create_all_scene_videos(
            run_directory=run_directory,
            scenes=storyboard.scenes,
        )
    )

    print(
        f"\nCreated {len(video_paths)} scene videos."
    )

    for video_path in video_paths:

        print(video_path)


if __name__ == "__main__":
    main()