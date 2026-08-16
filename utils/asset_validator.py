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
    def get_media_info(
        file_path: Path,
    ):

        if not AssetValidator.is_valid_file(
            file_path
        ):
            return None

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-show_entries",
            "stream=codec_type",
            "-of",
            "json",
            str(file_path),
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

            import json

            return json.loads(
                result.stdout
            )

        except (
            subprocess.CalledProcessError,
            ValueError,
        ):

            return None
    @staticmethod
    def get_duration(
        file_path: Path,
    ) -> float:

        info = AssetValidator.get_media_info(
            file_path
        )

        if not info:
            return 0.0

        try:

            return float(
                info["format"]["duration"]
            )

        except (
            KeyError,
            TypeError,
            ValueError,
        ):

            return 0.0

    @staticmethod
    def is_valid_media(
        file_path: Path,
    ) -> bool:

        info = AssetValidator.get_media_info(
            file_path
        )

        if not info:
            return False

        try:

            duration = float(
                info["format"]["duration"]
            )

            return duration > 0

        except (
            KeyError,
            TypeError,
            ValueError,
        ):

            return False

    @staticmethod
    def is_valid_audio(
        file_path: Path,
    ) -> bool:

        info = AssetValidator.get_media_info(
            file_path
        )

        if not info:
            return False

        streams = info.get(
            "streams",
            []
        )

        has_audio = any(
            stream.get("codec_type") == "audio"
            for stream in streams
        )

        return (
            has_audio
            and AssetValidator.is_valid_media(
                file_path
            )
        )

    @staticmethod
    def is_valid_video(
        file_path: Path,
    ) -> bool:

        info = AssetValidator.get_media_info(
            file_path
        )

        if not info:
            return False

        streams = info.get(
            "streams",
            []
        )

        has_video = any(
            stream.get("codec_type") == "video"
            for stream in streams
        )

        return (
            has_video
            and AssetValidator.is_valid_media(
                file_path
            )
        )

    @staticmethod
    def is_valid_video_with_audio(
        file_path: Path,
    ) -> bool:

        info = AssetValidator.get_media_info(
            file_path
        )

        if not info:
            return False

        streams = info.get(
            "streams",
            []
        )

        has_video = any(
            stream.get("codec_type") == "video"
            for stream in streams
        )

        has_audio = any(
            stream.get("codec_type") == "audio"
            for stream in streams
        )

        if not has_video or not has_audio:
            return False

        try:

            duration = float(
                info["format"]["duration"]
            )

            return duration > 0

        except (
            KeyError,
            TypeError,
            ValueError,
        ):

            return False