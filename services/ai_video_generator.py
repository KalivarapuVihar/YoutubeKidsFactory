import base64
import urllib.request
from pathlib import Path

from runwayml import RunwayML, TaskFailedError


class AIVideoGenerator:

    def __init__(
        self,
        model: str = "gen4_turbo",
    ):
        self.model = model
        self.client = RunwayML()

    @staticmethod
    def _image_to_data_uri(
        image_path: Path,
    ) -> str:

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image_bytes = image_path.read_bytes()

        if image_path.suffix.lower() == ".png":
            mime_type = "image/png"

        elif image_path.suffix.lower() in {
            ".jpg",
            ".jpeg",
        }:
            mime_type = "image/jpeg"

        else:
            raise ValueError(
                "Unsupported image format. "
                "Use PNG, JPG, or JPEG."
            )

        encoded = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        return (
            f"data:{mime_type};base64,{encoded}"
        )

    def generate(
    self,
    image_path: Path,
    output_path: Path,
    prompt: str,
    duration: int = 5,
    ratio: str = "1280:720",
    skip_existing: bool = True,
    ) -> Path:

        image_path = Path(image_path)
        output_path = Path(output_path)

        if duration < 2 or duration > 10:
            raise ValueError(
                "Runway video duration must be between 2 and 10 seconds."
            )

        if skip_existing and output_path.exists():
            file_size = (
                output_path.stat().st_size / (1024 * 1024)
            )

            print()
            print("AI motion video already exists.")
            print(
                f"Skipping Runway generation: {output_path}"
            )
            print(
                f"Existing video size: {file_size:.2f} MB"
            )
            print()

            return output_path

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        print()
        print("=" * 60)
        print("AI VIDEO GENERATION")
        print("=" * 60)
        print()
        print("Model:", self.model)
        print("Input:", image_path)
        print("Output:", output_path)
        print("Duration:", duration, "seconds")
        print("Ratio:", ratio)
        print()

        print("Motion prompt:")
        print("-" * 60)
        print(prompt)
        print("-" * 60)
        print()

        image_data_uri = self._image_to_data_uri(
            image_path
        )

        # -------------------------------------------------
        # Attempt 1: Original motion prompt
        # -------------------------------------------------

        prompts = [
            prompt,

            # Simpler fallback prompt.
            (
                "Preserve the exact characters, appearance, clothing, "
                "colors, proportions, environment and preschool 3D "
                "animation style of the input image. "

                f"Animate the characters naturally for {duration} seconds. "

                "Use smooth, gentle and believable movement. "
                "Keep faces, hands, arms, legs, bodies and identities stable. "
                "Show simple natural gestures and facial expressions. "

                "Preserve the existing environment and objects. "
                "Do not add characters or unrelated objects. "

                "Keep the original composition and main subjects clearly visible. "
                "No deformation, morphing, duplication, text, logos or watermark."
            )
        ]

        last_exception = None

        for attempt_number, current_prompt in enumerate(
            prompts,
            start=1,
        ):

            print()
            print(
                f"Submitting Runway attempt "
                f"{attempt_number}/{len(prompts)}..."
            )
            print()

            try:

                task = (
                    self.client.image_to_video.create(
                        model=self.model,
                        prompt_image=image_data_uri,
                        prompt_text=current_prompt,
                        ratio=ratio,
                        duration=duration,
                    )
                    .wait_for_task_output()
                )

                if not task.output:
                    raise RuntimeError(
                        "Runway task completed but returned "
                        "no video output."
                    )

                video_url = task.output[0]

                print()
                print(
                    "AI video generated successfully."
                )
                print(
                    "Video URL received."
                )
                print(
                    "Downloading video..."
                )
                print()

                urllib.request.urlretrieve(
                    video_url,
                    output_path,
                )

                if not output_path.exists():
                    raise RuntimeError(
                        "Video download failed."
                    )

                file_size = (
                    output_path.stat().st_size
                    / (1024 * 1024)
                )

                print(
                    f"Video saved: {output_path}"
                )
                print(
                    f"Video size: {file_size:.2f} MB"
                )
                print()

                print("=" * 60)
                print(
                    "AI VIDEO GENERATION COMPLETE"
                )
                print("=" * 60)
                print()

                return output_path

            except TaskFailedError as exc:

                last_exception = exc

                print()
                print(
                    f"Runway attempt {attempt_number} failed."
                )
                print()
                print(exc)

                if hasattr(
                    exc,
                    "task_details",
                ):
                    print()
                    print(
                        "Task details:",
                        exc.task_details,
                    )

                if attempt_number < len(prompts):

                    print()
                    print(
                        "Retrying with a simpler motion prompt..."
                    )
                    print()

            except Exception as exc:

                last_exception = exc

                print()
                print(
                    f"Runway attempt {attempt_number} "
                    f"encountered an error:"
                )
                print(exc)

                if attempt_number < len(prompts):

                    print()
                    print(
                        "Retrying with a simpler motion prompt..."
                    )
                    print()

        print()
        print("=" * 60)
        print("AI VIDEO GENERATION FAILED")
        print("=" * 60)
        print()
        print(
            "All Runway generation attempts failed."
        )
        print()

        if last_exception:
            raise last_exception

        raise RuntimeError(
            "Runway video generation failed."
        )