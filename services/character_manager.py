import json
from pathlib import Path
from typing import Dict, List

from models.character import Character


class CharacterManager:

    def __init__(
        self,
        characters_directory: Path,
    ):
        self.characters_directory = Path(
            characters_directory
        )

        self.characters: Dict[str, Character] = {}

        self._load_characters()

    def _load_characters(self):

        if not self.characters_directory.exists():
            raise FileNotFoundError(
                f"Characters directory not found: "
                f"{self.characters_directory}"
            )

        character_files = sorted(
            self.characters_directory.glob(
                "*.json"
            )
        )

        if not character_files:
            raise FileNotFoundError(
                "No character files found in "
                f"{self.characters_directory}"
            )

        for file_path in character_files:

            with open(
                file_path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

            character = Character.model_validate(
                data
            )

            key = character.name.lower()

            if key in self.characters:
                raise ValueError(
                    f"Duplicate character: "
                    f"{character.name}"
                )

            self.characters[key] = character

    def get_character(
        self,
        name: str,
    ) -> Character:

        key = name.lower().strip()

        if key not in self.characters:
            raise ValueError(
                f"Character not found: {name}"
            )

        return self.characters[key]

    def get_characters(
        self,
        names: List[str],
    ) -> List[Character]:

        return [
            self.get_character(name)
            for name in names
        ]

    def build_character_prompt(
        self,
        names: List[str],
    ) -> str:

        characters = self.get_characters(
            names
        )

        prompts = []

        for character in characters:

            prompts.append(
                character.character_prompt
            )

        return "\n\n".join(prompts)

    def get_reference_image(
        self,
        name: str,
    ) -> Path:

        character = self.get_character(
            name
        )

        filename = (
            f"{character.name.lower()}"
            "_reference.png"
        )

        reference_path = (
            self.characters_directory
            / filename
        )

        if not reference_path.exists():

            raise FileNotFoundError(
                "Reference image not found for "
                f"{character.name}: "
                f"{reference_path}"
            )

        return reference_path

    def get_reference_images(
        self,
        names: List[str],
    ) -> List[Path]:

        return [
            self.get_reference_image(name)
            for name in names
        ]

    def list_characters(self) -> List[str]:

        return [
            character.name
            for character in self.characters.values()
        ]