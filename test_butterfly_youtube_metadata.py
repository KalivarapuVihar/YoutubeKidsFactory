import json
from pathlib import Path

from models.lesson import Lesson
from services.openai_service import OpenAIService
from services.youtube_metadata_generator import (
    YouTubeMetadataGenerator,
)


def main():

    run = Path(
        "output/20260810_084916_butterflies"
    )

    lesson_path = (
        run / "lesson.json"
    )

    output_path = (
        run / "youtube_metadata.json"
    )

    print()
    print("=" * 60)
    print("BUTTERFLY YOUTUBE METADATA GENERATION")
    print("=" * 60)
    print()

    lesson_data = json.loads(
        lesson_path.read_text(
            encoding="utf-8"
        )
    )

    lesson = Lesson.model_validate(
        lesson_data
    )

    generator = YouTubeMetadataGenerator(
        OpenAIService()
    )

    metadata = generator.generate(
        topic=lesson.topic,
        introduction=lesson.introduction,
        examples=lesson.examples,
        activity_description=str(
            lesson.activity
        ),
        quiz_description=str(
            lesson.quiz
        ),
        song_title=lesson.song.title,
        song_mood=lesson.song.mood,
        existing_title=lesson.metadata.title,
        existing_description=(
            lesson.metadata.description
        ),
        existing_tags=lesson.metadata.tags,
    )

    output_path.write_text(
        json.dumps(
            metadata.model_dump(
                mode="json"
            ),
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("Metadata generated successfully.")
    print()
    print("Title:")
    print(metadata.title)
    print()
    print("Category:")
    print(metadata.category)
    print()
    print("Audience:")
    print(metadata.audience)
    print()
    print("Tags:")
    print(metadata.tags)
    print()
    print("Hashtags:")
    print(metadata.hashtags)
    print()
    print("Thumbnail concept:")
    print(metadata.thumbnail_concept)
    print()
    print(
        f"Saved to: {output_path}"
    )
    print()


if __name__ == "__main__":
    main()