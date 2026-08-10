from utils.run_manager import RunManager
from utils.file_manager import FileManager

from services.storyboard_generator import StoryboardGenerator
from services.image_generator import ImageGenerator
from services.voice_generator import VoiceGenerator


class ContentPipeline:

    def __init__(
        self,
        storyboard_generator: StoryboardGenerator,
        image_generator: ImageGenerator,
        voice_generator: VoiceGenerator,
    ):
        self.storyboard_generator = storyboard_generator
        self.image_generator = image_generator
        self.voice_generator = voice_generator

    def run(
        self,
        topic: str,
        lesson: str,
    ):

        metadata = RunManager.create_run(
            topic
        )

        storyboard = self.storyboard_generator.generate(
            topic=topic,
            lesson=lesson,
        )

        run_directory = RunManager.get_run_directory(
            metadata
        )

        storyboard_path = (
            run_directory / "storyboard.json"
        )

        FileManager.save_json(
            storyboard_path,
            storyboard.model_dump(
                mode="json"
            ),
        )

        # -------------------------
        # Generate Images
        # -------------------------

        images_directory = (
            run_directory / "images"
        )

        FileManager.ensure_directory(
            images_directory
        )

        for scene in storyboard.scenes:

            image_path = (
                images_directory
                / f"scene_{scene.scene_number:02d}.png"
            )

            if FileManager.file_exists(
                image_path
            ):
                print(
                    f"Skipping existing image: {image_path}"
                )
                continue

            self.image_generator.generate(
                scene=scene,
                output_path=image_path,
            )

        # -------------------------
        # Generate Voice
        # -------------------------

        voice_directory = (
            run_directory / "voice"
        )

        FileManager.ensure_directory(
            voice_directory
        )

        for scene in storyboard.scenes:

            voice_path = (
                voice_directory
                / f"scene_{scene.scene_number:02d}.mp3"
            )

            if FileManager.file_exists(
                voice_path
            ):
                print(
                    f"Skipping existing voice: {voice_path}"
                )
                continue

            self.voice_generator.generate(
                scene=scene,
                output_path=voice_path,
            )

        return metadata, storyboard