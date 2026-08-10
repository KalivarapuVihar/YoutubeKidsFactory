from pathlib import Path

from models.scene import Scene
from services.openai_service import OpenAIService


class VoiceGenerator:

    def __init__(
        self,
        ai_service: OpenAIService,
    ):
        self.ai_service = ai_service

    def generate(
        self,
        scene: Scene,
        output_path: Path,
    ) -> str:

        return self.ai_service.generate_speech(
            text=scene.narration,
            output_path=output_path,
        )