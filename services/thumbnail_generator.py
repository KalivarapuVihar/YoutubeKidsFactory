from pathlib import Path

from models.thumbnail import ThumbnailConcept
from models.youtube_metadata import YouTubeMetadata
from services.openai_service import OpenAIService
from services.character_manager import CharacterManager


class ThumbnailGenerator:

    def __init__(
        self,
        ai_service: OpenAIService,
        character_manager: CharacterManager,
    ):

        self.ai_service = ai_service
        self.character_manager = character_manager

    def generate_concept(
        self,
        episode_title: str,
        topic: str,
        characters: list,
        learning_objective: str,
    ) -> ThumbnailConcept:

        prompt = f"""
You are the creative director for a premium
preschool animation YouTube channel called
Wonderland Valley.

Create ONE highly compelling YouTube
thumbnail concept.

EPISODE:
{episode_title}

TOPIC:
{topic}

LEARNING OBJECTIVE:
{learning_objective}

CHARACTERS:
{", ".join(characters)}

TARGET AUDIENCE:
Children ages 2-6 and their parents.

THUMBNAIL STRATEGY:

Use:

- ONE primary recurring character
- ONE strong facial expression
- ONE important story object
- Simple colorful environment
- Strong foreground/background separation
- Large recognizable shapes
- Clear visual storytelling
- Premium preschool 3D animation

The thumbnail must communicate the episode
idea immediately at a small size.

IMPORTANT:

Do not create a cluttered composition.

Do not use many characters.

Do not use arrows.

Do not use red circles.

Do not use misleading clickbait.

Prefer NO TEXT.

Do not redesign the recurring characters.

Preserve their established appearance.

The result should look like a premium
children's animated series rather than a
generic AI-generated image.

Return structured data only.
"""

        return self.ai_service.generate_structured(
            prompt=prompt,
            response_model=ThumbnailConcept,
        )

    def build_image_prompt(
        self,
        concept: ThumbnailConcept,
    ) -> str:

        character_prompt = (
            self.character_manager
            .build_character_prompt(
                [concept.main_character]
            )
        )

        return f"""
Create a premium YouTube thumbnail for a
preschool animated educational series.

CHANNEL:
Wonderland Valley

EPISODE:
{concept.episode_title}

CANONICAL CHARACTER:

{character_prompt}

THUMBNAIL CONCEPT:

Main Character:
{concept.main_character}

Supporting Character:
{concept.supporting_character or "None"}

Main Object:
{concept.main_object}

Character Emotion:
{concept.character_emotion}

Background:
{concept.background}

Composition:
{concept.composition}

Visual Hook:
{concept.visual_hook}

CHARACTER CONSISTENCY:

The supplied character reference image is
the canonical design.

Do not redesign, rename, recolor, replace,
or merge the character.

Maintain:

- face
- hairstyle or fur
- body proportions
- skin/fur colors
- clothing
- accessories
- species
- recognizable identity
- established 3D animation style

THUMBNAIL STYLE:

High-quality premium preschool 3D animation.

Bright cheerful environment.

Soft rounded shapes.

Warm cinematic lighting.

Strong expressive facial emotion.

Large readable shapes.

Clear focal point.

Strong foreground/background separation.

Clean composition.

Designed specifically for a YouTube
thumbnail and readable at small size.

Avoid:

- text
- logos
- watermarks
- arrows
- red circles
- clutter
- character duplication
- extra limbs
- distorted faces
- photorealism
- scary imagery

The image must feel like an official
Wonderland Valley production asset.
"""

    def generate_image(
        self,
        concept: ThumbnailConcept,
        output_path: Path,
    ) -> str:

        reference_paths = (
            self.character_manager
            .get_reference_images(
                [concept.main_character]
            )
        )

        prompt = self.build_image_prompt(
            concept
        )

        return (
            self.ai_service
            .generate_image_with_references(
                prompt=prompt,
                reference_paths=reference_paths,
                output_path=output_path,
            )
        )

    def generate_from_metadata(
        self,
        metadata: YouTubeMetadata,
        output_path: Path,
    ) -> str:

        concept = ThumbnailConcept(
            episode_title=metadata.title,
            main_character="Maya",
            supporting_character=None,
            main_object=(
                metadata.thumbnail_concept
            ),
            character_emotion=(
                "Surprised and delighted"
            ),
            background=(
                "Bright magical Wonderland Valley "
                "environment"
            ),
            composition=(
                "Maya large in the foreground "
                "interacting with the main story "
                "object"
            ),
            visual_hook=(
                metadata.thumbnail_concept
            ),
            image_prompt=(
                metadata.thumbnail_concept
            ),
        )

        return self.generate_image(
            concept=concept,
            output_path=output_path,
        )