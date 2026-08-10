from utils.run_manager import RunManager


def main():

    run = RunManager(
        "Butterflies"
    )

    run.initialize()

    print(
        f"Run directory: {run.root}"
    )

    print(
        f"Images: {run.images_dir}"
    )

    print(
        f"Voice: {run.voice_dir}"
    )

    print(
        f"Video: {run.video_dir}"
    )

    print(
        f"Lesson: {run.lesson_path}"
    )

    print(
        f"Storyboard: {run.storyboard_path}"
    )

    print(
        f"Final video: {run.final_video_path}"
    )


if __name__ == "__main__":
    main()