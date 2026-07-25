from openai import OpenAI
from typing import TypeVar, Type
from pydantic import BaseModel

from config.settings import (
    AI_MODEL,
    OPENAI_API_KEY,
)
from utils.logger import logger

T = TypeVar("T", bound=BaseModel)   

class OpenAIService:

    def __init__(self):

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. Please check your .env file."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

        logger.info("OpenAI client initialized.")

    def generate_text(self, prompt: str) -> str:

        logger.info("Sending request to OpenAI.")

        try:

            response = self.client.responses.create(
                model=AI_MODEL,
                input=prompt,
            )

            logger.info("Response received successfully.")

            return response.output_text

        except Exception as error:

            logger.exception(
                f"OpenAI request failed: {error}"
            )

            raise

    def generate_structured(self,prompt: str,response_model: Type[T],) -> T:

        logger.info("Sending structured request to OpenAI.")

        try:

            response = self.client.responses.parse(
                model=AI_MODEL,
                input=prompt,
                text_format=response_model,
            )

            logger.info("Structured response received.")

            return response.output_parsed

        except Exception as error:

            logger.exception(
                f"Structured generation failed: {error}"
            )

            raise