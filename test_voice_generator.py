from pathlib import Path

from services.openai_service import OpenAIService
from services.voice_generator import VoiceGenerator


def main():

    ai_service = OpenAIService()

    generator = VoiceGenerator(
        ai_service
    )

    output_path = Path(
        "output/test_voice.mp3"
    )

    class TestScene:

        narration = (
            "Hello little explorers! "
            "Today we are learning about butterflies."
        )

    generator.generate(
        scene=TestScene(),
        output_path=output_path,
    )

    print(
        f"\nVoice created successfully: {output_path}"
    )


if __name__ == "__main__":
    main()