from pathlib import Path
import subprocess

from utils.logger import logger
from utils.asset_validator import AssetValidator


class VideoRenderer:

    @staticmethod
    def create_scene_video(
        image_path: Path,
        audio_path: Path,
        output_path: Path,
    ) -> str:

        logger.info(
            f"Creating video segment: {output_path}"
        )

        command = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(image_path),
            "-i",
            str(audio_path),
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-c:a",
            "aac",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            str(output_path),
        ]

        try:

            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

            logger.info(
                f"Video segment created: {output_path}"
            )

            return str(output_path)

        except subprocess.CalledProcessError as error:

            logger.error(
                "FFmpeg video generation failed."
            )

            logger.error(
                error.stderr
            )

            raise

    @staticmethod
    def create_all_scene_videos(
        run_directory: Path,
        scenes,
    ) -> list[Path]:

        images_directory = (
            run_directory / "images"
        )

        voice_directory = (
            run_directory / "voice"
        )

        video_directory = (
            run_directory / "video"
        )

        video_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        video_paths = []

        for scene in scenes:

            image_path = (
                images_directory
                / f"scene_{scene.scene_number:02d}.png"
            )

            audio_path = (
                voice_directory
                / f"scene_{scene.scene_number:02d}.mp3"
            )

            output_path = (
                video_directory
                / f"scene_{scene.scene_number:02d}.mp4"
            )

            if AssetValidator.is_valid_media(
                output_path
            ):

                logger.info(
                    f"Skipping existing video: "
                    f"{output_path}"
                )

                video_paths.append(
                    output_path
                )

                continue

            if output_path.exists():

                logger.warning(
                    f"Existing video is invalid. "
                    f"Regenerating: {output_path}"
                )

                output_path.unlink()

            VideoRenderer.create_scene_video(
                image_path=image_path,
                audio_path=audio_path,
                output_path=output_path,
            )

            video_paths.append(
                output_path
            )

        return video_paths

    @staticmethod
    def concatenate_videos(video_paths: list[Path],output_path: Path,) -> str:   
        logger.info(
            f"Concatenating "
            f"{len(video_paths)} video segments."
        )

        concat_file = (
            output_path.parent / "concat.txt"
        )

        with open(
            concat_file,
            "w",
            encoding="utf-8",
        ) as file:

            for video_path in video_paths:

                resolved_path = (
                    video_path.resolve()
                )

                # Use an unquoted absolute path.
                # This avoids problems with apostrophes
                # in directory or file names.
                file.write(
                    f"file {resolved_path}\n"
                )

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output_path),
        ]

        try:

            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

            logger.info(
                f"Final video created: {output_path}"
            )

            return str(output_path)

        except subprocess.CalledProcessError as error:

            logger.error(
                "FFmpeg video concatenation failed."
            )

            logger.error(
                error.stderr
            )

            raise