from pathlib import Path

from services.video_renderer import VideoRenderer


def main():

    video_files = sorted(
        Path("output").glob(
            "*/video/scene_*.mp4"
        )
    )

    if not video_files:
        raise FileNotFoundError(
            "No scene videos found."
        )

    # Get the run directory from the first scene video
    run_directory = (
        video_files[0]
        .parent
        .parent
    )

    video_directory = (
        run_directory / "video"
    )

    video_paths = sorted(
        video_directory.glob(
            "scene_*.mp4"
        )
    )

    if not video_paths:
        raise FileNotFoundError(
            f"No scene videos found in {video_directory}"
        )

    output_path = (
        run_directory / "final_video.mp4"
    )

    print(
        f"Run directory: {run_directory}"
    )

    print(
        f"Found {len(video_paths)} scene videos."
    )

    VideoRenderer.concatenate_videos(
        video_paths=video_paths,
        output_path=output_path,
    )

    print(
        f"\nFinal video created: {output_path}"
    )


if __name__ == "__main__":
    main()