from datetime import datetime
from email.mime import text
from importlib import metadata
from pathlib import Path
import re

from config.settings import OUTPUT_DIR
from enums.run_status import RunStatus
from models.run_metadata import RunMetadata
from utils.file_manager import FileManager


class RunManager:

    @staticmethod
    def _slugify(text: str) -> str:

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9]+",
            "_",
            text
        )

        return text.strip("_")

    @staticmethod
    def _generate_run_id() -> str:

        return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
        )

    @classmethod
    def create_run(
        cls,
        topic: str
    ) -> RunMetadata:
        run_id = cls._generate_run_id()

        slug = cls._slugify(topic)

        folder_name = f"{run_id}_{slug}"

        run_folder = OUTPUT_DIR / folder_name

        FileManager.ensure_directory(run_folder)

        for folder in [
            "images",
            "voice",
            "video",
            "thumbnail",
        ]:
            FileManager.ensure_directory(
                run_folder / folder
            )
        now = datetime.now()

        metadata = RunMetadata(
            run_id=run_id,
            topic=topic,
            status=RunStatus.CREATED,
            created_at=now,
            updated_at=now,
        )

        FileManager.save_json(
        run_folder / "metadata.json",
        metadata.model_dump(
                mode="json"
            ),
        )
        return metadata

    @classmethod
    def get_run_directory(
        cls,
        metadata: RunMetadata,
    ) -> Path:

        slug = cls._slugify(
            metadata.topic
        )

        folder_name = f"{metadata.run_id}_{slug}"

        return OUTPUT_DIR / folder_name

        