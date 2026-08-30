from pathlib import Path
import subprocess

from utils.logger import logger
from utils.asset_validator import AssetValidator
from services.ai_video_generator import AIVideoGenerator
from services.ai_motion_prompt_generator import AIMotionPromptGenerator
from services.motion_video_compositor import MotionVideoCompositor


class VideoRenderer:

    @staticmethod
    def create_scene_video(
        motion_path: Path,
        audio_path: Path,
        output_path: Path,
    ) -> str:

        logger.info(
            f"Creating final scene video: {output_path}"
        )

        MotionVideoCompositor.create_scene_video(
            motion_path=motion_path,
            voice_path=audio_path,
            output_path=output_path,
        )

        return str(output_path)

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

        motion_directory = (
            video_directory / "motion_scenes"
        )

        video_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        motion_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ---------------------------------
        # Runway AI Video Generator
        # ---------------------------------

        ai_video_generator = AIVideoGenerator(
            model="gen4_turbo"
        )

        video_paths = []

        for scene in scenes:

            scene_number = scene.scene_number

            image_path = (
                images_directory
                / f"scene_{scene_number:02d}.png"
            )

            audio_path = (
                voice_directory
                / f"scene_{scene_number:02d}.mp3"
            )

            motion_path = (
                motion_directory
                / f"scene_{scene_number:02d}.mp4"
            )

            output_path = (
                video_directory
                / f"scene_{scene_number:02d}.mp4"
            )

            # ---------------------------------
            # Validate source assets
            # ---------------------------------

            if not image_path.exists():
                raise FileNotFoundError(
                    f"Scene image not found: {image_path}"
                )

            if not audio_path.exists():
                raise FileNotFoundError(
                    f"Scene voice not found: {audio_path}"
                )

            # ---------------------------------
            # Generate REAL AI MOTION
            # ---------------------------------

            if AssetValidator.is_valid_media(
                motion_path
            ):

                logger.info(
                    f"Skipping existing Runway motion: "
                    f"{motion_path}"
                )

            else:

                if motion_path.exists():

                    logger.warning(
                        f"Existing motion video is invalid. "
                        f"Regenerating: {motion_path}"
                    )

                    motion_path.unlink()

                logger.info(
                    f"Generating Runway motion for "
                    f"scene {scene_number}..."
                )

                motion_prompt = (
                    AIMotionPromptGenerator.generate(
                        scene
                    )
                )

                duration = int(
                    round(scene.duration_seconds)
                )

                # Runway supports 2-10 seconds.
                duration = max(
                    2,
                    min(duration, 10),
                )

                ai_video_generator.generate(
                    image_path=image_path,
                    output_path=motion_path,
                    prompt=motion_prompt,
                    duration=duration,
                    ratio="1280:720",
                    skip_existing=False,
                )

            # ---------------------------------
            # Combine Runway motion + voice
            # ---------------------------------

            if AssetValidator.is_valid_media(
                output_path
            ):

                logger.info(
                    f"Skipping existing final scene video: "
                    f"{output_path}"
                )

                video_paths.append(
                    output_path
                )

                continue

            if output_path.exists():

                logger.warning(
                    f"Existing scene video is invalid. "
                    f"Regenerating: {output_path}"
                )

                output_path.unlink()

            VideoRenderer.create_scene_video(
                motion_path=motion_path,
                audio_path=audio_path,
                output_path=output_path,
            )

            video_paths.append(
                output_path
            )

        return video_paths

    @staticmethod
    def create_brand_intro(
        video_path: Path,
        audio_path: Path,
        output_path: Path,
    ) -> Path:

        video_path = Path(video_path)
        audio_path = Path(audio_path)
        output_path = Path(output_path)

        if not video_path.exists():
            raise FileNotFoundError(
                f"Brand intro video not found: {video_path}"
            )

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Brand intro audio not found: {audio_path}"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            f"Creating branded intro: {output_path}"
        )

        # Keep the complete 10-second branding video.
        # If the audio is shorter, pad the remaining time
        # with silence rather than cutting the video short.

        command = [
            "ffmpeg",
            "-y",

            "-i",
            str(video_path),

            "-i",
            str(audio_path),

            "-filter_complex",
            (
                "[1:a]"
                "apad="
                "pad_dur=10.083333,"
                "atrim=duration=10.083333,"
                "asetpts=PTS-STARTPTS[a]"
            ),

            "-map",
            "0:v:0",
            "-map",
            "[a]",

            "-t",
            "10.083333",

            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",

            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-ar",
            "24000",
            "-ac",
            "1",

            "-movflags",
            "+faststart",

            str(output_path),
        ]

        try:

            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

        except subprocess.CalledProcessError as error:

            logger.error(
                "Failed to create branded intro."
            )

            logger.error(
                error.stderr
            )

            raise

        if not output_path.exists():

            raise RuntimeError(
                "Failed to create branded intro video."
            )

        logger.info(
            f"Branded intro created: {output_path}"
        )

        return output_path

    @staticmethod
    def concatenate_videos(
        video_paths: list[Path],
        output_path: Path,
    ) -> str:

        logger.info(
            f"Concatenating "
            f"{len(video_paths)} video segments."
        )

        if not video_paths:
            raise ValueError(
                "No video paths provided for concatenation."
            )

        for video_path in video_paths:
            if not video_path.exists():
                raise FileNotFoundError(
                    f"Video not found: {video_path}"
                )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ---------------------------------
        # Branding assets
        # ---------------------------------

        branding_video = Path(
            "data/branding/wonderland_valley_intro.mp4"
        )

        branding_audio = Path(
            "data/branding/wonderland_valley_intro.mp3"
        )

        branded_intro = (
            output_path.parent
            / "wonderland_valley_intro_with_audio.mp4"
        )

        # ---------------------------------
        # Create branded intro if needed
        # ---------------------------------

        if not branded_intro.exists():

            logger.info(
                "Branded intro does not exist. "
                "Creating it..."
            )

            VideoRenderer.create_brand_intro(
                video_path=branding_video,
                audio_path=branding_audio,
                output_path=branded_intro,
            )

        else:

            logger.info(
                f"Using existing branded intro: "
                f"{branded_intro}"
            )

        # ---------------------------------
        # Final video order
        #
        # Branding intro appears exactly once
        # before Scene 1.
        # ---------------------------------

        final_video_paths = [
            branded_intro,
            *video_paths,
        ]

        logger.info(
            f"Final video contains "
            f"{len(final_video_paths)} segments "
            f"(including branding intro)."
        )

        # ---------------------------------
        # Create concat file
        # ---------------------------------

        concat_file = (
            output_path.parent / "concat.txt"
        )

        with open(
            concat_file,
            "w",
            encoding="utf-8",
        ) as file:

            for video_path in final_video_paths:

                resolved_path = (
                    video_path.resolve()
                )

                escaped_path = (
                    str(resolved_path)
                    .replace("'", "'\\''")
                )

                file.write(
                    f"file '{escaped_path}'\n"
                )

        # ---------------------------------
        # Concatenate
        # ---------------------------------

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-ar",
            "24000",
            "-ac",
            "1",
            "-movflags",
            "+faststart",
            str(output_path),
        ]

        try:

            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )

        except subprocess.CalledProcessError as error:

            logger.error(
                "FFmpeg video concatenation failed."
            )

            logger.error(
                error.stderr
            )

            raise

        if not output_path.exists():

            raise RuntimeError(
                "Final video was not created."
            )

        logger.info(
            f"Final video created: {output_path}"
        )

        return str(output_path)