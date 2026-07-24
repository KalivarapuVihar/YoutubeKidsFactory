from openai import OpenAI

from config.settings import OPENAI_API_KEY
from config.settings import AI_MODEL
from utils.logger import logger

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

        logger.info("OpenAI client initialized.")

    def generate_text(self,prompt):

        logger.info("Sending test request to OpenAI.")

        try:
            response = self.client.responses.create(
                model=AI_MODEL,
                input=prompt
            )

            logger.info("Response received.")

            return response.output_text
        
        except Exception as error:
            logger.exception(f"Error during OpenAI request: {error}")
            raise
