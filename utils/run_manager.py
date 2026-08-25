from datetime import datetime
from pathlib import Path
from typing import Optional
import json
import re

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
                self.sanitize_topic(
                    topic
                )
            )

            self.root = (
                OUTPUT_DIR
                / f"{timestamp}_{safe_topic}"
            )

        # ---------------------------------
        # Asset directories
        # ---------------------------------

        self.images_dir = (
            self.root / "images"
        )

        self.voice_dir = (
            self.root / "voice"
        )

        self.video_dir = (
            self.root / "video"
        )

        # ---------------------------------
        # Core pipeline files
        # ---------------------------------

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

        self.captions_path = (
            self.root / "captions.srt"
        )

        # ---------------------------------
        # YouTube files
        # ---------------------------------

        self.youtube_metadata_path = (
            self.root
            / "youtube_metadata.json"
        )

        self.thumbnail_path = (
            self.root
            / "thumbnail.jpg"
        )

        self.youtube_result_path = (
            self.root
            / "youtube_result.json"
        )

    # ---------------------------------
    # Topic / directory helpers
    # ---------------------------------

    @staticmethod
    def sanitize_topic(
        topic: str,
    ) -> str:

        """
        Convert a topic into a safe filesystem
        directory name.

        Examples:

        Maya's Rainbow Mystery
        ->
        mayas_rainbow_mystery

        Why Does a Rainbow Appear?
        ->
        why_does_a_rainbow_appear

        Let's Learn Colors & Shapes!
        ->
        lets_learn_colors_shapes
        """

        safe_topic = topic.strip().lower()

        # Replace apostrophes by removing them rather
        # than turning them into underscores.
        safe_topic = safe_topic.replace(
            "'",
            "",
        )

        # Replace every remaining sequence of
        # non-alphanumeric characters with "_".
        safe_topic = re.sub(
            r"[^a-z0-9]+",
            "_",
            safe_topic,
        )

        # Remove leading/trailing underscores.
        safe_topic = safe_topic.strip(
            "_"
        )

        # Prevent excessively long directory names.
        safe_topic = safe_topic[:100].rstrip(
            "_"
        )

        if not safe_topic:

            safe_topic = "untitled"

        return safe_topic

    # ---------------------------------
    # Directory initialization
    # ---------------------------------

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

    # ---------------------------------
    # Metadata
    # ---------------------------------

    def create_metadata(self):

        if self.metadata_path.exists():
            return

        metadata = {
            "topic": self.topic,
            "status": "created",
            "scenes": 0,
            "created_at": (
                datetime.now().isoformat()
            ),
            "updated_at": (
                datetime.now().isoformat()
            ),
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

    def update_metadata(
        self,
        **updates,
    ):

        if self.metadata_path.exists():

            with open(
                self.metadata_path,
                "r",
                encoding="utf-8",
            ) as file:

                metadata = json.load(
                    file
                )

        else:

            metadata = {
                "topic": self.topic,
                "created_at": (
                    datetime.now().isoformat()
                ),
            }

        metadata.update(
            updates
        )

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

    # ---------------------------------
    # Existing run detection
    # ---------------------------------

    @staticmethod
    def find_existing_run(
        topic: str,
    ):

        safe_topic = (
            RunManager.sanitize_topic(
                topic
            )
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

            has_captions = (
                run / "captions.srt"
            ).exists()

            has_youtube_metadata = (
                run / "youtube_metadata.json"
            ).exists()

            has_youtube_result = (
                run / "youtube_result.json"
            ).exists()

            if (
                has_lesson
                or has_storyboard
                or has_images
                or has_voice
                or has_video
                or has_final_video
                or has_captions
                or has_youtube_metadata
                or has_youtube_result
            ):

                return run

        return None