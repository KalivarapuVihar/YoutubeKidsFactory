from models.thumbnail import ThumbnailConcept


def main():

    thumbnail = ThumbnailConcept(
        episode_title=(
            "Maya's Missing Butterfly"
        ),
        main_character="Maya",
        supporting_character=None,
        main_object="Colorful butterfly",
        character_emotion=(
            "Surprised and delighted"
        ),
        background=(
            "Bright magical flower garden "
            "in Wonderland Valley"
        ),
        composition=(
            "Maya large in the foreground "
            "looking toward a large butterfly "
            "flying toward the camera"
        ),
        visual_hook=(
            "A beautiful oversized butterfly "
            "flies directly toward Maya"
        ),
        image_prompt=(
            "Premium preschool 3D animated "
            "YouTube thumbnail featuring Maya, "
            "a 5-year-old Indian-inspired but "
            "globally appealing preschool girl "
            "with her established Wonderland "
            "Valley appearance, looking "
            "surprised and delighted as a "
            "beautiful colorful butterfly flies "
            "toward the camera. Bright magical "
            "flower garden, simple clean "
            "composition, expressive face, "
            "large recognizable shapes, "
            "cinematic children's animation, "
            "polished high-quality 3D style, "
            "vibrant cheerful environment, "
            "strong foreground/background "
            "separation, premium children's "
            "YouTube thumbnail."
        ),
    )

    print()
    print("=" * 60)
    print("THUMBNAIL CONCEPT TEST")
    print("=" * 60)
    print()

    print(
        "Episode:",
        thumbnail.episode_title,
    )

    print(
        "Main character:",
        thumbnail.main_character,
    )

    print(
        "Emotion:",
        thumbnail.character_emotion,
    )

    print(
        "Main object:",
        thumbnail.main_object,
    )

    print()
    print("Visual hook:")
    print(thumbnail.visual_hook)

    print()
    print("Image prompt:")
    print(thumbnail.image_prompt)

    print()
    print(
        "Thumbnail concept validation successful."
    )


if __name__ == "__main__":
    main()