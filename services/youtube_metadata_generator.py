from models.youtube_metadata import (
    YouTubeMetadata,
)
from models.episode import Episode
from services.openai_service import OpenAIService


class YouTubeMetadataGenerator:

    def __init__(
        self,
        ai_service: OpenAIService,
    ):
        self.ai_service = ai_service

    def generate(
        self,
        episode: Episode,
    ) -> YouTubeMetadata:

        prompt = f"""
You are a YouTube growth strategist
specializing in high-quality preschool
educational animation channels.

Create YouTube metadata for this episode.

CHANNEL:
Wonderland Valley

TARGET AUDIENCE:
Children ages 2-6 and their parents.

EPISODE TITLE:
{episode.title}

TOPIC:
{episode.topic}

LEARNING OBJECTIVE:
{episode.learning_objective}

RECURRING PHRASE:
{episode.recurring_phrase}

CHARACTERS:
{", ".join(episode.characters)}

Create metadata optimized for:

- discoverability
- parent search intent
- children's educational content
- strong click-through potential
- accurate expectations
- long-term channel growth

IMPORTANT:

Do not use misleading clickbait.

Do not keyword-stuff.

Do not claim educational outcomes
that are not present in the episode.

The title should be natural and appealing.

The description should clearly explain
what children will learn.

The thumbnail concept should be visually
simple and readable at small size.

Return structured data only.
"""

        return self.ai_service.generate_structured(
            prompt=prompt,
            response_model=YouTubeMetadata,
        )