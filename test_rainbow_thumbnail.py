import json
from pathlib import Path

from models.youtube_metadata import YouTubeMetadata
from services.openai_service import OpenAIService
from services.thumbnail_generator import ThumbnailGenerator
from services.character_manager import CharacterManager


def main():

    run = Path(
        "output/20260818_222639_mayas_rainbow_mystery"
    )

    metadata_path = (
        run / "youtube_metadata.json"
    )

    output_path = (
        run / "thumbnail.jpg"
    )

    metadata = YouTubeMetadata.model_validate(
        json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )
    )

    print()
    print("=" * 60)
    print("RAINBOW YOUTUBE THUMBNAIL GENERATION")
    print("=" * 60)
    print()

    print(
        "Episode:",
        metadata.title,
    )

    print(
        "Thumbnail concept:"
    )

    print(
        metadata.thumbnail_concept
    )

    print()

    generator = ThumbnailGenerator(
        ai_service=OpenAIService(),
        character_manager=CharacterManager(
            Path("data/characters")
        ),
    )

    print(
        "Generating Rainbow thumbnail..."
    )

    generator.generate_from_metadata(
        metadata=metadata,
        output_path=output_path,
    )

    print()
    print("=" * 60)
    print("THUMBNAIL GENERATION SUCCESSFUL")
    print("=" * 60)
    print()

    print(
        "Thumbnail:",
        output_path,
    )

    print(
        "Thumbnail exists:",
        output_path.exists(),
    )

    if output_path.exists():
        print(
            "Thumbnail size:",
            f"{output_path.stat().st_size / (1024 * 1024):.2f} MB",
        )

    print()


if __name__ == "__main__":
    main()