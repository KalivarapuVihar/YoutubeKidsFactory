from models.scene import Scene


class AIMotionPromptGenerator:

    @staticmethod
    def generate(scene: Scene) -> str:

        characters = ", ".join(scene.characters)
        duration = scene.duration_seconds

        prompt = (
            f"Preserve the exact characters, appearance, clothing, "
            f"colors, proportions, environment, objects and preschool "
            f"3D style of the input image.\n\n"

            f"Animate this scene naturally for {duration} seconds.\n\n"

            f"CHARACTERS: {characters}\n"
            f"ACTION: {scene.action}\n"
            f"EMOTION: {scene.emotion}\n"
            f"CAMERA: {scene.camera}\n\n"

            "MOTION DIRECTION:\n"
            "The animation must visually perform the described action. "
            "Do not substitute unrelated movements. "
            "Character gestures should correspond to what the scene "
            "is communicating. "
            "When characters count, point toward or interact with each "
            "counted object in sequence. "
            "When an object is added, removed, moved or discovered, "
            "show that action clearly. "
            "When a character asks the viewer a question, have the "
            "character face or gesture toward the viewer and allow a "
            "brief natural thinking moment. "
            "When a character discovers something, use an appropriate "
            "reaction such as looking, pointing, leaning closer or "
            "showing gentle surprise.\n\n"

            "IMPORTANT MOTION RULES:\n"
            "- Keep all original characters consistent.\n"
            "- Animate characters continuously during active moments.\n"
            "- Use visible body and facial movement appropriate to the action.\n"
            "- Keep movement gentle and preschool-friendly.\n"
            "- Keep faces, hands, limbs, bodies and identity stable.\n"
            "- Do not morph, duplicate or remove characters.\n"
            "- Do not create extra limbs or distorted hands.\n"
            "- Do not add unrelated objects.\n"
            "- Do not remove or duplicate educational objects.\n"
            "- Preserve the original environment.\n"
            "- Preserve the original composition.\n"
            "- Keep important objects visible when they are being discussed.\n"
            "- No text, logos or watermark."
        ).strip()

        if len(prompt) > 1000:
            prompt = prompt[:997].rstrip() + "..."

        return prompt