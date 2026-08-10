from pathlib import Path

from services.openai_service import OpenAIService
from services.image_generator import ImageGenerator


def main():

    ai_service = OpenAIService()

    generator = ImageGenerator(
        ai_service
    )

    output_path = Path(
        "output/test_image.png"
    )

    prompt = """
    A cute colorful butterfly flying over
    a sunny flower garden, preschool educational
    cartoon illustration, cheerful friendly style,
    bright colors, rounded shapes, no text,
    no letters, no numbers, no logos,
    no watermark.
    """

    class TestScene:
        image_prompt = prompt

    generator.generate(
        scene=TestScene(),
        output_path=output_path,
    )

    print(
        f"\nImage created successfully: {output_path}"
    )


if __name__ == "__main__":
    main()