from pathlib import Path

from models.scene import Scene
from services.openai_service import OpenAIService
from services.character_manager import CharacterManager


class ImageGenerator:

    def __init__(
        self,
        ai_service: OpenAIService,
        character_manager: CharacterManager,
    ):
        self.ai_service = ai_service
        self.character_manager = character_manager

    def generate(
        self,
        scene: Scene,
        output_path: Path,
    ) -> str:

        character_prompt = (
            self.character_manager.build_character_prompt(
                scene.characters
            )
        )

        reference_paths = (
            self.character_manager.get_reference_images(
                scene.characters
            )
        )

        enhanced_prompt = f"""

Create a polished production-quality frame
from a premium preschool animated series
called Wonderland Valley.

SECTION:

{scene.section}

CHARACTER CONSISTENCY REQUIREMENTS:

{character_prompt}

The supplied reference images are the canonical
visual designs of the characters.

Preserve their identity and visual appearance.

Do not redesign, rename, recolor, replace,
or merge the characters.

Maintain:

- facial features
- hairstyle or fur
- body proportions
- skin/fur colors
- clothing
- accessories
- species
- character scale
- overall 3D animation style

SCENE:

Location:

{scene.location}

Characters:

{", ".join(scene.characters)}

Action:

{scene.action}

Emotion:

{scene.emotion}

Camera:

{scene.camera}

Original Scene Prompt:

{scene.image_prompt}

VISUAL STORYTELLING:

The image should clearly communicate what is
happening in this scene to a preschool child.

Show the characters actively participating in
the story rather than simply standing or posing.

If the scene involves child interaction,
discovery, questioning, pointing, observing,
counting, choosing, explaining or responding,
make that action visually obvious.

Important educational objects and environmental
elements described in the scene should be clearly
visible and easy for a child to understand.

VISUAL STYLE:

High-quality preschool 3D animation.

Bright vibrant colors.

Soft rounded shapes.

Warm cinematic lighting.

Expressive child-friendly faces.

Beautiful readable composition.

Safe and appealing for children ages 2-6.

Create a complete scene composition,
not a character reference sheet.

The characters should interact naturally
with the environment and with each other.

Avoid:

- text
- letters
- numbers
- logos
- watermarks
- character duplication
- extra limbs
- distorted faces
- unrelated characters
- unrelated objects
- photorealism

Maintain visual continuity with the
Wonderland Valley universe.
""".strip()

        return self.ai_service.generate_image_with_references(
            prompt=enhanced_prompt,
            reference_paths=reference_paths,
            output_path=output_path,
        )