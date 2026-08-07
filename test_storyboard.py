from models.scene import Scene
from models.storyboard import Storyboard


scene1 = Scene(
    scene_number=1,
    narration="Hello children! Today we are learning about butterflies.",
    image_prompt="A cute colorful butterfly flying over flowers, preschool cartoon style, bright cheerful colors, no text.",
    duration_seconds=6,
)

scene2 = Scene(
    scene_number=2,
    narration="Butterflies start their lives as tiny eggs.",
    image_prompt="A tiny butterfly egg on a green leaf, friendly preschool educational cartoon illustration, bright colors, no text.",
    duration_seconds=7,
)


storyboard = Storyboard(
    topic="Butterflies",
    scenes=[
        scene1,
        scene2,
    ],
)


print(
    storyboard.model_dump_json(
        indent=4
    )
)