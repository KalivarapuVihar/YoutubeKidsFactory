import json

from services.openai_service import OpenAIService
from services.lesson_generator import LessonGenerator
from services.storyboard_generator import StoryboardGenerator
from services.image_generator import ImageGenerator
from services.voice_generator import VoiceGenerator
from services.video_renderer import VideoRenderer

from utils.run_manager import RunManager
from utils.file_manager import FileManager


def main():

    topic = "Butterflies"

    # ---------------------------------
    # Create run
    # ---------------------------------

    existing_run = RunManager.find_existing_run(
    topic
    )

    if existing_run:

        print()
        print(
            f"Existing run found: {existing_run}"
        )
        print(
            "Resuming existing run..."
        )

        run = RunManager(
            topic=topic,
            run_directory=existing_run,
        )

    else:

        print()
        print(
            "No existing run found."
        )
        print(
            "Creating a new run..."
        )

        run = RunManager(
            topic=topic
        )

    run.initialize()

    print()
    print(f"Run directory: {run.root}")
    print()

    # ---------------------------------
    # Initialize services
    # ---------------------------------

    ai_service = OpenAIService()

    lesson_generator = LessonGenerator(
        ai_service
    )

    storyboard_generator = StoryboardGenerator(
        ai_service
    )

    image_generator = ImageGenerator(
        ai_service
    )

    voice_generator = VoiceGenerator(
        ai_service
    )

    # ---------------------------------
    # Lesson
    # ---------------------------------

    if run.lesson_path.exists():

        print(
            "Lesson already exists. "
            "Skipping generation."
        )

        lesson_data = FileManager.read_json(
            run.lesson_path
        )

        from models.lesson import Lesson

        lesson = Lesson.model_validate(
            lesson_data
        )

    else:

        print("Generating lesson...")

        lesson = lesson_generator.generate(
            topic=topic
        )

        FileManager.save_json(
            run.lesson_path,
            lesson.model_dump()
        )

        print(
            "Lesson generated successfully."
        )

    # ---------------------------------
    # Storyboard
    # ---------------------------------

    if run.storyboard_path.exists():

        print(
            "Storyboard already exists. "
            "Skipping generation."
        )

        from models.storyboard import Storyboard

        storyboard_data = (
            FileManager.read_json(
                run.storyboard_path
            )
        )

        storyboard = Storyboard.model_validate(
            storyboard_data
        )

    else:

        print("Generating storyboard...")

        storyboard = (
            storyboard_generator.generate(
                topic=lesson.topic,
                lesson=lesson.introduction,
            )
        )

        FileManager.save_json(
            run.storyboard_path,
            storyboard.model_dump()
        )

        print(
            f"Storyboard generated with "
            f"{len(storyboard.scenes)} scenes."
        )

    # ---------------------------------
    # Images + Voice
    # ---------------------------------

    print()
    print("Generating scene assets...")
    print()

    for scene in storyboard.scenes:

        scene_number = scene.scene_number

        image_path = (
            run.images_dir
            / f"scene_{scene_number:02d}.png"
        )

        voice_path = (
            run.voice_dir
            / f"scene_{scene_number:02d}.mp3"
        )

        # Image

        if image_path.exists():

            print(
                f"Skipping image {scene_number}"
            )

        else:

            print(
                f"Generating image {scene_number}..."
            )

            image_generator.generate(
                scene=scene,
                output_path=image_path,
            )

        # Voice

        if voice_path.exists():

            print(
                f"Skipping voice {scene_number}"
            )

        else:

            print(
                f"Generating voice {scene_number}..."
            )

            voice_generator.generate(
                scene=scene,
                output_path=voice_path,
            )

    print()
    print("All scene assets ready.")

    # ---------------------------------
    # Scene Videos
    # ---------------------------------

    print()
    print("Generating scene videos...")
    print()

    video_paths = (
        VideoRenderer.create_all_scene_videos(
            run_directory=run.root,
            scenes=storyboard.scenes,
        )
    )

    print(
        f"Created {len(video_paths)} scene videos."
    )

    # ---------------------------------
    # Final Video
    # ---------------------------------

    if run.final_video_path.exists():

        print(
            "Final video already exists. "
            "Skipping concatenation."
        )

    else:

        print()
        print("Creating final video...")

        VideoRenderer.concatenate_videos(
            video_paths=video_paths,
            output_path=run.final_video_path,
        )

        print(
            "Final video created successfully."
        )

    print()
    print("=" * 50)
    print("PIPELINE COMPLETED")
    print("=" * 50)
    print()
    print(
        f"Final video: {run.final_video_path}"
    )


if __name__ == "__main__":
    main()