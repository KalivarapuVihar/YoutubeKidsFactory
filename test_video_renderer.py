from pathlib import Path

from services.video_renderer import VideoRenderer


def main():

    image_files = sorted(
        Path("output").glob("*/images/scene_01.png")
    )

    if not image_files:
        raise FileNotFoundError(
            "Could not find scene_01.png"
        )

    image_path = image_files[-1]

    run_directory = image_path.parent.parent

    audio_path = (
        run_directory
        / "voice"
        / "scene_01.mp3"
    )

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Could not find audio file: {audio_path}"
        )

    output_path = (
        run_directory
        / "scene_01.mp4"
    )

    print(f"Image: {image_path}")
    print(f"Audio: {audio_path}")
    print(f"Output: {output_path}")

    VideoRenderer.create_scene_video(
        image_path=image_path,
        audio_path=audio_path,
        output_path=output_path,
    )

    print(
        f"\nVideo created successfully: {output_path}"
    )


if __name__ == "__main__":
    main()