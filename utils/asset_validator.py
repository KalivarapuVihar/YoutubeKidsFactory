from pathlib import Path
import subprocess


class AssetValidator:

    @staticmethod
    def is_valid_file(
        file_path: Path,
    ) -> bool:

        return (
            file_path.exists()
            and file_path.is_file()
            and file_path.stat().st_size > 0
        )

    @staticmethod
    def is_valid_json(
        file_path: Path,
    ) -> bool:

        if not AssetValidator.is_valid_file(
            file_path
        ):
            return False

        try:

            import json

            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as file:

                json.load(file)

            return True

        except Exception:

            return False

    @staticmethod
    def is_valid_media(
        file_path: Path,
    ) -> bool:

        if not AssetValidator.is_valid_file(
            file_path
        ):
            return False

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file_path),
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

            duration = float(
                result.stdout.strip()
            )

            return duration > 0

        except (
            subprocess.CalledProcessError,
            ValueError,
        ):

            return False