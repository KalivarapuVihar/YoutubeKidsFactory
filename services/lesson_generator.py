from models.lesson import Lesson
from services.openai_service import OpenAIService
from utils.prompt_manager import PromptManager


class LessonGenerator:

    def __init__(
        self,
        ai_service: OpenAIService,
    ):
        self.ai_service = ai_service

    def generate(
        self,
        topic: str,
    ) -> Lesson:

        prompt = PromptManager.load_prompt(
            "lesson_prompt.txt",
            topic=topic,
        )

        lesson = (
            self.ai_service.generate_structured(
                prompt=prompt,
                response_model=Lesson,
            )
        )

        return lesson