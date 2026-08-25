from pathlib import Path

from services.motion_video_compositor import (
    MotionVideoCompositor,
)


def main():

    run = Path(
        "output/20260818_222639_mayas_rainbow_mystery"
    )

    video_dir = run / "video"
    voice_dir = run / "voice"
    scene_dir = video_dir / "motion_scenes"

    scene_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("=" * 70)
    print("MOTION + NARRATION COMPOSITOR")
    print("=" * 70)
    print()

    created = 0
    skipped = 0

    for scene_number in range(1, 9):

        motion_path = (
            video_dir
            / f"scene_{scene_number:02d}_motion.mp4"
        )

        voice_path = (
            voice_dir
            / f"scene_{scene_number:02d}.mp3"
        )

        output_path = (
            scene_dir
            / f"scene_{scene_number:02d}.mp4"
        )

        print()
        print("=" * 70)
        print(
            f"SCENE {scene_number} / 8"
        )
        print("=" * 70)

        if output_path.exists():

            print(
                f"Already exists: {output_path}"
            )

            skipped += 1
            continue

        MotionVideoCompositor.create_scene_video(
            motion_path=motion_path,
            voice_path=voice_path,
            output_path=output_path,
        )

        created += 1

    print()
    print("=" * 70)
    print("COMPOSITING COMPLETE")
    print("=" * 70)
    print()
    print(
        f"New scene videos: {created}"
    )
    print(
        f"Skipped existing: {skipped}"
    )
    print()

    for scene_number in range(1, 9):

        path = (
            scene_dir
            / f"scene_{scene_number:02d}.mp4"
        )

        if path.exists():
            print(
                f"OK  {path}"
            )
        else:
            print(
                f"MISSING  {path}"
            )

    print()


if __name__ == "__main__":
    main()