from services.openai_service import OpenAIService

from services.storyboard_generator import StoryboardGenerator

from pipeline.content_pipeline import ContentPipeline


def main():

    ai_service = OpenAIService()

    storyboard_generator = StoryboardGenerator(
        ai_service
    )

    pipeline = ContentPipeline(
        storyboard_generator
    )

    metadata, storyboard = pipeline.run(
        topic="Butterflies",
        lesson="""
        Butterflies are colorful insects.
        They begin life as eggs.
        They become caterpillars.
        Then they form a chrysalis.
        Finally, they become butterflies.
        """
    )

    print("\nRun ID:")
    print(metadata.run_id)

    print("\nStoryboard:")
    print(
        storyboard.model_dump_json(
            indent=4
        )
    )


if __name__ == "__main__":
    main()