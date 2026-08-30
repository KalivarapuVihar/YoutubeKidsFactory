from pathlib import Path
import re
from config.settings import VOICE_ASSIGNMENTS

from models.scene import Scene
from services.openai_service import OpenAIService


class VoiceGenerator:

    def __init__(
        self,
        ai_service: OpenAIService,
    ):
        self.ai_service = ai_service

    @staticmethod
    def remove_speaker_label(
        text: str,
    ) -> str:

        text = str(text).strip()

        if not text:
            return ""

        # Remove speaker labels such as:
        #
        # Maya: Hello!
        # Milo: Wow!
        # Pip: Look at that!
        # Tia: Let's learn!
        #
        # Only remove a label at the beginning
        # of the dialogue line.

        text = re.sub(
            r"^[A-Za-z][A-Za-z0-9 _-]{0,40}:\s*",
            "",
            text,
        )

        return text.strip()

    @staticmethod
    def parse_dialogue_line(text: str):
        text = str(text).strip()

        match = re.match(
            r"^([A-Za-z][A-Za-z0-9 _-]{0,40}):\s*(.*)$",
            text,
        )

        if match:
            speaker = match.group(1).strip()
            dialogue = match.group(2).strip()
            return speaker, dialogue

        return "Maya", text

    @staticmethod
    def get_voice_instructions(
        speaker: str,
    ) -> str:

        instructions = {
            "Maya": (
                "Warm, caring preschool teacher and friendly adventure guide. "
                "Speak naturally and conversationally, with bright energy. "
                "Use expressive emphasis, gentle curiosity, playful surprise, "
                "and encouraging warmth. Vary pacing naturally. "
                "Use short pauses after questions and before important discoveries. "
                "Do not sound like a news narrator, audiobook reader, or formal lecturer."
            ),

            "Milo": (
                "Young playful boy character. Clearly different from the adult narrator. "
                "Energetic, curious and spontaneous. "
                "Use a youthful, playful delivery with noticeable excitement, "
                "quick reactions, natural surprise and short enthusiastic phrases. "
                "Vary pitch and pacing naturally. "
                "Do not sound like a narrator or teacher."
            ),

            "Pip": (
                "Tiny cheerful playful character. Light, bright and bouncy personality. "
                "Sound curious and delighted when discovering something. "
                "Use short expressive reactions, playful energy and natural variation "
                "in pitch and pacing. Make the voice clearly distinct from Maya and Milo. "
                "Do not sound like a narrator."
            ),

            "Tia": (
                "Sweet, bright and playful young girl character. "
                "Friendly, curious and expressive. "
                "Use gentle excitement, childlike wonder, natural surprise "
                "and varied pacing. Make the voice clearly distinct from Maya, Milo "
                "and the narrator. Do not sound like a formal narrator."
            ),

            "Narrator": (
                "Warm children's storytelling narrator. "
                "Speak like an engaging storyteller talking directly to preschool children, "
                "not like someone reading a script or newspaper. "
                "Use natural pauses, varied pacing, expressive emphasis and gentle wonder. "
                "Slow slightly before important learning moments and discoveries. "
                "Use a warm, inviting tone and occasional playful energy. "
                "Avoid monotone delivery, formal narration, audiobook style and news-reader style."
            ),
        }

        return instructions.get(
            speaker,
            instructions["Maya"],
        )

    @staticmethod
    def build_voice_segments(scene: Scene):
        segments = []

        for line in scene.dialogue:
            if not line:
                continue

            speaker, dialogue = (
                VoiceGenerator.parse_dialogue_line(line)
            )

            if not dialogue:
                continue

            voice = VOICE_ASSIGNMENTS.get(
                speaker,
                VOICE_ASSIGNMENTS["Maya"],
            )   

            segments.append({
                "speaker": speaker,
                "text": dialogue,
                "voice": voice,
                "instructions": VoiceGenerator.get_voice_instructions(
                    speaker
                )
            })

        if (
            scene.narration
            and scene.narration.strip()
        ):
            segments.append({
                "speaker": "Narrator",
                "text": scene.narration.strip(),
                "voice": "shimmer",
                "instructions": VoiceGenerator.get_voice_instructions(
                    "Narrator"
                ),
            })

        return segments

    def generate(
        self,
        scene: Scene,
        output_path: Path,
    ) -> str:

        segments = self.build_voice_segments(scene)

        if not segments:
            raise ValueError(
                f"Scene {scene.scene_number} has no "
                "dialogue or narration for voice generation."
            )

        output_path = Path(output_path)

        segment_directory = (
            output_path.parent
            / f"scene_{scene.scene_number:02d}_segments"
        )

        segment_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        segment_paths = []

        for index, segment in enumerate(segments):

            segment_path = (
                segment_directory
                / f"segment_{index:02d}.mp3"
            )

            self.ai_service.generate_speech(
                text=segment["text"],
                output_path=segment_path,
                voice=segment["voice"],
                instructions=segment["instructions"],
            )

            segment_paths.append(segment_path)

        # Create concat file
        concat_file = (
            segment_directory / "concat.txt"
        )

        with open(
            concat_file,
            "w",
            encoding="utf-8",
        ) as file:

            for segment_path in segment_paths:
                file.write(
                    f"file '{segment_path.resolve()}'\n"
                )

        import subprocess

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c:a",
                "libmp3lame",
                "-b:a",
                "128k",
                str(output_path),
            ],
            check=True,
        )

        return str(output_path)