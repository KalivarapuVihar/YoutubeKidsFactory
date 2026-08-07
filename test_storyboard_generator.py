from services.openai_service import OpenAIService
from services.storyboard_generator import StoryboardGenerator


def main():

    ai_service = OpenAIService()

    generator = StoryboardGenerator(
        ai_service
    )

    storyboard = generator.generate(
        topic="Butterflies",
        lesson="""
        Butterflies are colorful insects.
        They begin life as eggs.
        They become caterpillars.
        Then they form a chrysalis.
        Finally, they become butterflies.
        """
    )

    print(
        storyboard.model_dump_json(
            indent=4
        )
    )


if __name__ == "__main__":
    main()