from datetime import datetime
from pathlib import Path
from typing import Optional

from config.settings import OUTPUT_DIR


class RunManager:

    def __init__(
        self,
        topic: str,
        run_directory: Optional[Path] = None,
    ):

        self.topic = topic

        if run_directory:

            self.root = Path(
                run_directory
            )

        else:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            safe_topic = (
                topic.lower()
                .replace(" ", "_")
            )

            self.root = (
                OUTPUT_DIR
                / f"{timestamp}_{safe_topic}"
            )

        self.images_dir = (
            self.root / "images"
        )

        self.voice_dir = (
            self.root / "voice"
        )

        self.video_dir = (
            self.root / "video"
        )

        self.lesson_path = (
            self.root / "lesson.json"
        )

        self.storyboard_path = (
            self.root / "storyboard.json"
        )

        self.final_video_path = (
            self.root / "final_video.mp4"
        )

    def initialize(self):

        self.images_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.voice_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.video_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def find_existing_run(
        topic: str,
    ):

        safe_topic = (
            topic.lower()
            .replace(" ", "_")
        )

        pattern = (
            f"*_{safe_topic}"
        )

        runs = sorted(
            OUTPUT_DIR.glob(pattern),
            reverse=True,
        )

        for run in runs:

            if not run.is_dir():
                continue

            # Only consider a run resumable if
            # it contains at least one pipeline artifact.

            has_lesson = (
                run / "lesson.json"
            ).exists()

            has_storyboard = (
                run / "storyboard.json"
            ).exists()

            has_images = (
                (run / "images").exists()
                and any(
                    (run / "images").iterdir()
                )
            )

            has_voice = (
                (run / "voice").exists()
                and any(
                    (run / "voice").iterdir()
                )
            )

            has_video = (
                (run / "video").exists()
                and any(
                    (run / "video").iterdir()
                )
            )

            has_final_video = (
                run / "final_video.mp4"
            ).exists()

            if (
                has_lesson
                or has_storyboard
                or has_images
                or has_voice
                or has_video
                or has_final_video
            ):
                return run

        return None
