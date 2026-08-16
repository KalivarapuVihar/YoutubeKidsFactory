import json
from pathlib import Path
from models.character import Character

directory = Path("data/characters")

for path in sorted(directory.glob("*.json")):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    character = Character.model_validate(data)

    print(
        f"Valid: {character.name} "
        f"({character.species})"
    )

print("All character files validated successfully.")