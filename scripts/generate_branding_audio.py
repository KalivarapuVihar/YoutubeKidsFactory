from pathlib import Path
import sys


# Add project root to Python import path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from services.openai_service import OpenAIService


OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "branding"
    / "wonderland_valley_intro.mp3"
)


INTRO_SCRIPT = (
    "Welcome to Wonderland Valley! "
    "Come explore, learn, and discover "
    "something amazing with us!"
)


def main():

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("=" * 60)
    print("GENERATING WONDERLAND VALLEY INTRO AUDIO")
    print("=" * 60)
    print()
    print("Model: gpt-4o-mini-tts")
    print("Voice: alloy")
    print()
    print("Script:")
    print(INTRO_SCRIPT)
    print()

    ai_service = OpenAIService()

    ai_service.generate_speech(
        text=INTRO_SCRIPT,
        output_path=OUTPUT_PATH,
    )

    print()
    print("=" * 60)
    print("INTRO AUDIO GENERATED")
    print("=" * 60)
    print()
    print(f"Saved: {OUTPUT_PATH}")
    print()


if __name__ == "__main__":
    main()