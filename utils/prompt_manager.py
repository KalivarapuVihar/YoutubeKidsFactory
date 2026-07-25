from pathlib import Path

from utils.file_manager import FileManager

class PromptManager:

    PROMPTS_DIR = Path("prompts")
    
    @classmethod
    def load_prompt(
        cls,
        filename: str,
        **kwargs
    ) -> str:

        prompt_path = cls.PROMPTS_DIR / filename

        template = FileManager.read_text(
            prompt_path
        )

        return template.format(**kwargs)