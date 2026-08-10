from datetime import datetime
from pathlib import Path
from typing import Optional

from config.settings import OUTPUT_DIR
import json

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
        self.metadata_path = (
            self.root / "metadata.json"
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

    def create_metadata(self):

        if self.metadata_path.exists():
            return

        metadata = {
            "topic": self.topic,
            "status": "created",
            "scenes": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        with open(
            self.metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
            )


    def update_metadata(self, **updates):

        if self.metadata_path.exists():

            with open(
                self.metadata_path,
                "r",
                encoding="utf-8",
            ) as file:

                metadata = json.load(file)

        else:

            metadata = {
                "topic": self.topic,
                "created_at": datetime.now().isoformat(),
            }

        metadata.update(updates)

        metadata["updated_at"] = (
            datetime.now().isoformat()
        )

        with open(
            self.metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
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
