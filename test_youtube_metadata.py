from models.youtube_metadata import (
    YouTubeMetadata,
)


def main():

    metadata = YouTubeMetadata(
        title=(
            "Maya's Missing Butterfly 🦋 | "
            "Learn the Butterfly Life Cycle"
        ),
        description=(
            "Join Maya and her friends on a "
            "fun adventure as they discover "
            "how a butterfly grows from an egg "
            "into a caterpillar, chrysalis and "
            "beautiful butterfly."
        ),
        tags=[
            "butterfly life cycle",
            "butterflies for kids",
            "kids learning",
            "preschool learning",
            "science for kids",
            "animals for kids",
            "educational videos for kids",
        ],
        hashtags=[
            "#WonderlandValley",
            "#ButterfliesForKids",
            "#KidsLearning",
            "#PreschoolLearning",
        ],
        thumbnail_concept=(
            "Maya looking amazed as a colorful "
            "butterfly flies toward her, with "
            "bright flowers and a large butterfly "
            "in the foreground."
        ),
        learning_objective=(
            "Children learn the four basic stages "
            "of the butterfly life cycle."
        ),
    )

    print()
    print("=" * 60)
    print("YOUTUBE METADATA MODEL TEST")
    print("=" * 60)

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
    print("Thumbnail:")
    print(metadata.thumbnail_concept)

    print()
    print("Metadata model validation successful.")


if __name__ == "__main__":
    main()