from models.scene import Scene


class AIMotionPromptGenerator:

    @staticmethod
    def generate(scene: Scene) -> str:

        characters = ", ".join(scene.characters)

        prompt = f"""
Preserve the exact characters, appearance, clothing,
colors, proportions, environment, lighting and preschool
3D animation style of the input image.

Animate this scene naturally for 5 seconds.

CHARACTERS:
{characters}

ACTION:
{scene.action}

EMOTION:
{scene.emotion}

MOTION:
Make the characters perform the described action with
smooth, gentle and believable preschool-friendly movement.
Keep faces, hands, arms, legs and bodies stable.
No character deformation, morphing, duplication or identity changes.

ENVIRONMENT:
Add only subtle natural movement such as a gentle breeze,
grass movement, small water movement or soft particles.
Keep the rainbow and important background elements stable.

CAMERA:
{scene.camera}
Use only a gentle, stable camera movement.

Keep the original composition and main subjects clearly visible.
Do not introduce new characters or objects.

No text, letters, numbers, logos or watermark.
""".strip()

        # Runway promptText maximum is 1000 characters.
        if len(prompt) > 950:
            prompt = (
                f"Preserve the exact characters, appearance, "
                f"clothing, colors, proportions and preschool "
                f"3D style of the input image. "
                f"Animate naturally for 5 seconds.\n\n"
                f"Characters: {characters}\n"
                f"Action: {scene.action}\n"
                f"Emotion: {scene.emotion}\n\n"
                f"Make the characters perform the action with "
                f"smooth gentle movement. Keep faces, hands, "
                f"limbs and bodies stable. No deformation, "
                f"morphing, duplication or identity changes.\n\n"
                f"Add only subtle environmental movement. "
                f"Keep important background elements stable.\n"
                f"Camera: {scene.camera}\n\n"
                f"Keep the original composition. "
                f"No new characters or objects. "
                f"No text, logos or watermark."
            ).strip()

        # Final safety check.
        if len(prompt) > 1000:
            raise ValueError(
                f"Runway motion prompt is too long: "
                f"{len(prompt)} characters"
            )

        return prompt