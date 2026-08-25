from pathlib import Path
import subprocess


class MotionVideoCompositor:

    @staticmethod
    def get_duration(path: Path) -> float:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return float(result.stdout.strip())

    @staticmethod
    def create_scene_video(
        motion_path: Path,
        voice_path: Path,
        output_path: Path,
    ) -> Path:

        motion_path = Path(motion_path)
        voice_path = Path(voice_path)
        output_path = Path(output_path)

        if not motion_path.exists():
            raise FileNotFoundError(
                f"Motion video not found: {motion_path}"
            )

        if not voice_path.exists():
            raise FileNotFoundError(
                f"Voice file not found: {voice_path}"
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        motion_duration = (
            MotionVideoCompositor.get_duration(
                motion_path
            )
        )

        voice_duration = (
            MotionVideoCompositor.get_duration(
                voice_path
            )
        )

        print()
        print(
            f"Motion: {motion_duration:.3f}s"
        )
        print(
            f"Voice:  {voice_duration:.3f}s"
        )

        # If voice is longer than the generated
        # motion clip, freeze the final video frame
        # for the remaining duration.
        if voice_duration > motion_duration:

            extra = (
                voice_duration - motion_duration
            )

            print(
                f"Extending final frame by "
                f"{extra:.3f}s"
            )

            filter_complex = (
                f"[0:v]tpad=stop_mode=clone:"
                f"stop_duration={extra:.3f},"
                f"trim=duration={voice_duration:.3f},"
                f"setpts=PTS-STARTPTS[v]"
            )

        else:

            filter_complex = (
                f"[0:v]trim=duration={voice_duration:.3f},"
                f"setpts=PTS-STARTPTS[v]"
            )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(motion_path),
            "-i",
            str(voice_path),
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "1:a",
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
            "-shortest",
            str(output_path),
        ]

        subprocess.run(
            command,
            check=True,
        )

        if not output_path.exists():
            raise RuntimeError(
                f"Failed to create scene video: "
                f"{output_path}"
            )

        print(
            f"Scene video created: {output_path}"
        )

        return output_path