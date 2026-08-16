from pathlib import Path

from services.character_manager import CharacterManager

manager = CharacterManager(
    Path("data/characters")
)

print(
    "Characters:",
    manager.list_characters()
)

maya = manager.get_character("Maya")

print(
    "Maya role:",
    maya.role
)

prompt = manager.build_character_prompt(
    ["Maya", "Milo"]
)

print()
print("Character prompt:")
print(prompt)

print()
print("CharacterManager test successful.")