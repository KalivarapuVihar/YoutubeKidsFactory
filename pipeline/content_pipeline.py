from utils.run_manager import RunManager
from utils.file_manager import FileManager

from services.storyboard_generator import StoryboardGenerator


class ContentPipeline:

    def __init__(
        self,
        storyboard_generator: StoryboardGenerator,
    ):
        self.storyboard_generator = storyboard_generator

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

        return metadata, storyboard