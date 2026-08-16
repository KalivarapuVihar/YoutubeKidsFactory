from pathlib import Path
from typing import List


class CaptionGenerator:

    @staticmethod
    def format_timestamp(
        seconds: float,
    ) -> str:

        total_milliseconds = round(
            seconds * 1000
        )

        hours = (
            total_milliseconds
            // 3_600_000
        )

        remaining = (
            total_milliseconds
            % 3_600_000
        )

        minutes = (
            remaining
            // 60_000
        )

        remaining = (
            remaining
            % 60_000
        )

        secs = (
            remaining
            // 1000
        )

        milliseconds = (
            remaining
            % 1000
        )

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d},"
            f"{milliseconds:03d}"
        )

    @staticmethod
    def generate_srt(
        scenes,
        scene_durations: List[float],
        output_path: Path,
    ) -> str:

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        current_time = 0.0

        caption_blocks = []

        caption_number = 1

        for scene, duration in zip(
            scenes,
            scene_durations,
        ):

            caption_text = (
                getattr(
                    scene,
                    "caption_text",
                    None,
                )
                or ""
            ).strip()

            if not caption_text:
                current_time += duration
                continue

            start_time = current_time

            end_time = (
                current_time
                + duration
            )

            start_timestamp = (
                CaptionGenerator.format_timestamp(
                    start_time
                )
            )

            end_timestamp = (
                CaptionGenerator.format_timestamp(
                    end_time
                )
            )

            block = (
                f"{caption_number}\n"
                f"{start_timestamp} --> "
                f"{end_timestamp}\n"
                f"{caption_text}\n"
            )

            caption_blocks.append(
                block
            )

            caption_number += 1

            current_time += duration

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "\n".join(
                    caption_blocks
                )
            )

        return str(output_path)