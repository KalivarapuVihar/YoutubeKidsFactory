from typing import List

from services.openai_service import OpenAIService
from models.youtube_metadata import YouTubeMetadata


class YouTubeMetadataGenerator:

    def __init__(
        self,
        ai_service: OpenAIService,
    ):
        self.ai_service = ai_service

    def generate(
        self,
        topic: str,
        introduction: str,
        examples: List[str],
        activity_description: str,
        quiz_description: str,
        song_title: str,
        song_mood: str,
        existing_title: str,
        existing_description: str,
        existing_tags: List[str],
    ) -> YouTubeMetadata:

        prompt = f"""
You are a YouTube growth strategist
specializing in high-quality preschool
educational animation channels.

Create YouTube metadata for a Wonderland
Valley preschool educational episode.

CHANNEL:
Wonderland Valley

TARGET AUDIENCE:
Children ages 2-6 and their parents.

TOPIC:
{topic}

INTRODUCTION:
{introduction}

EXAMPLES:
{", ".join(examples)}

ACTIVITY:
{activity_description}

QUIZ:
{quiz_description}

SONG:
{song_title}

SONG MOOD:
{song_mood}

EXISTING TITLE:
{existing_title}

EXISTING DESCRIPTION:
{existing_description}

EXISTING TAGS:
{", ".join(existing_tags)}

Create metadata optimized for:

- discoverability
- parent search intent
- preschool educational content
- strong click-through potential
- accurate expectations
- long-term channel growth
- natural language

IMPORTANT:

Do not use misleading clickbait.

Do not keyword-stuff.

Do not claim educational outcomes
that are not present in the episode.

Keep the title natural and appealing.

The description should clearly explain
what children will learn.

Generate relevant search tags.

Generate useful hashtags.

The thumbnail concept should be visually
simple and readable at small size.

The thumbnail concept should preferably
feature one recurring Wonderland Valley
character with a strong facial expression
and one important story object.

The content is made for children ages 2-6.

Return structured data only.
"""

        return self.ai_service.generate_structured(
            prompt=prompt,
            response_model=YouTubeMetadata,
        )