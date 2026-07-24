from pathlib import Path
import json

from utils.logger import logger

class FileManager:
    @staticmethod
    def ensure_directory(directory):
        Path(directory).mkdir(parents=True, exist_ok=True)

    def save_text(file_path, content):
        FileManager.ensure_directory(Path(file_path).parent)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        logger.info(f"Saved Text file to {file_path}")

    @staticmethod
    def read_text(file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    @staticmethod
    def save_json(file_path, data):

        FileManager.ensure_directory(
            Path(file_path).parent
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        logger.info(f"Saved JSON file: {file_path}")

    @staticmethod
    def read_json(file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    @staticmethod
    def file_exists(file_path):

        return Path(file_path).exists()

    