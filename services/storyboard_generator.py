from models.storyboard import Storyboard
from services.openai_service import OpenAIService
from utils.prompt_manager import PromptManager


class StoryboardGenerator:

    def __init__(self, ai_service: OpenAIService):
        self.ai_service = ai_service

    def generate(
        self,
        topic: str,
        lesson: str,
    ) -> Storyboard:

        prompt = PromptManager.load_prompt(
            "storyboard_prompt.txt",
            topic=topic,
            lesson=lesson,
        )

        storyboard = self.ai_service.generate_structured(
            prompt=prompt,
            response_model=Storyboard,
        )

        return storyboard