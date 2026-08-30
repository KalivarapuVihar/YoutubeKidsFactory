from typing import Type, TypeVar, List
import httpx

from openai import OpenAI
from pydantic import BaseModel
from config.settings import VOICE_MODEL, VOICE_ASSIGNMENTS

from config.settings import (
    AI_MODEL,
    OPENAI_API_KEY,
    IMAGE_MODEL,
    VOICE_MODEL,
    VOICE_NAME,
)
from utils.logger import logger


T = TypeVar(
    "T",
    bound=BaseModel,
)


class OpenAIService:

    def __init__(self):

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. "
                "Please check your .env file."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            timeout=httpx.Timeout(
                300.0,
            connect=30.0,
            ),
             max_retries=2,  
        )

        logger.info(
            "OpenAI client initialized."
        )

    def generate_text(
        self,
        prompt: str,
    ) -> str:

        logger.info(
            "Sending request to OpenAI."
        )

        try:

            response = self.client.responses.create(
                model=AI_MODEL,
                input=prompt,
            )

            logger.info(
                "Response received successfully."
            )

            return response.output_text

        except Exception as error:

            logger.exception(
                f"OpenAI request failed: {error}"
            )

            raise

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
    ) -> T:

        logger.info(
            "Sending structured request to OpenAI."
        )

        try:

            response = self.client.responses.parse(
                model=AI_MODEL,
                input=prompt,
                text_format=response_model,
            )

            logger.info(
                "Structured response received."
            )

            return response.output_parsed

        except Exception as error:

            logger.exception(
                f"Structured generation failed: {error}"
            )

            raise

    def generate_image(
        self,
        prompt: str,
        output_path,
    ) -> str:

        logger.info(
            "Sending image generation request to OpenAI."
        )

        try:

            response = self.client.images.generate(
                model=IMAGE_MODEL,
                prompt=prompt,
                size="1536x1024",
            )

            image_data = response.data[0]

            if not image_data.b64_json:
                raise ValueError(
                    "Image generation returned "
                    "no image data."
                )

            import base64

            image_bytes = base64.b64decode(
                image_data.b64_json
            )

            with open(
                output_path,
                "wb",
            ) as file:

                file.write(image_bytes)

            logger.info(
                f"Image saved successfully: "
                f"{output_path}"
            )

            return str(output_path)

        except Exception as error:

            logger.exception(
                f"Image generation failed: {error}"
            )

            raise

    def generate_image_with_references(
        self,
        prompt: str,
        reference_paths: List,
        output_path,
    ) -> str:

        logger.info(
            "Sending reference-based image "
            "generation request to OpenAI."
        )

        reference_files = []

        try:

            for reference_path in reference_paths:

                file = open(
                    reference_path,
                    "rb",
                )

                reference_files.append(
                    file
                )

            response = self.client.images.edit(
                model=IMAGE_MODEL,
                image=reference_files,
                prompt=prompt,
                size="1536x1024",
                quality="medium",
                input_fidelity="high",
            )

            image_data = response.data[0]

            if not image_data.b64_json:
                raise ValueError(
                    "Reference-based image generation "
                    "returned no image data."
                )

            import base64

            image_bytes = base64.b64decode(
                image_data.b64_json
            )

            with open(
                output_path,
                "wb",
            ) as file:

                file.write(image_bytes)

            logger.info(
                "Reference-based image saved: "
                f"{output_path}"
            )

            return str(output_path)

        except Exception as error:

            logger.exception(
                "Reference-based image generation failed: "
                f"{error}"
            )

            raise

        finally:

            for file in reference_files:

                file.close()

    def generate_speech(
        self,
        text: str,
        output_path,
        voice: str = None,
        instructions: str = None,
    ) -> str:

        selected_voice = voice

        logger.info(
            "Sending text-to-speech request to OpenAI."
        )

        try:

            response = self.client.audio.speech.create(
                model=VOICE_MODEL,
                voice=selected_voice,
                input=text,
                instructions=instructions,
            )

            response.write_to_file(
                output_path
            )

            logger.info(
                f"Voice file saved successfully: "
                f"{output_path}"
            )

            return str(output_path)

        except Exception as error:

            logger.exception(
                f"Speech generation failed: {error}"
            )

            raise