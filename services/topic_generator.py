from services.openai_service import OpenAIService
from utils.prompt_manager import PromptManager


class TopicGenerator:

    def __init__(self, ai_service: OpenAIService):
        self.ai_service = ai_service

    def generate(self) -> str:
        prompt = PromptManager.load_prompt(
            "topic_prompt.txt",
            age_group="2-5 years",
            language="English",
            category="General Knowledge"
        )
        topic = self.ai_service.generate_text(prompt)

        return topic.strip()