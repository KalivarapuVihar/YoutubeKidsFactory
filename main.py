from pathlib import Path
from services.openai_service import OpenAIService
from services.lesson_generator import LessonGenerator
from services.storyboard_generator import StoryboardGenerator
from services.image_generator import ImageGenerator
from services.voice_generator import VoiceGenerator
from services.video_renderer import VideoRenderer
from services.character_manager import CharacterManager
from utils.caption_generator import CaptionGenerator

from utils.run_manager import RunManager
from utils.file_manager import FileManager
from utils.asset_validator import AssetValidator

def main():

    topic = input(
    "Enter topic for the video: "
    ).strip()

    if not topic:
        raise ValueError(
        "Topic cannot be empty."
    )

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
    run.create_metadata()

    print()
    print(f"Run directory: {run.root}")
    print()

    # ---------------------------------
    # Initialize services
    # ---------------------------------

    ai_service = OpenAIService()

    character_manager = CharacterManager(
        Path("data/characters")
    )

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

        run.update_metadata(
                    status="lesson_completed",
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
        run.update_metadata(
            scenes=len(storyboard.scenes),
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

        run.update_metadata(
            status="storyboard_completed",
            scenes=len(storyboard.scenes),
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

        if AssetValidator.is_valid_file(image_path):

            print(
                f"Skipping valid image {scene_number}"
            )

        else:

            if image_path.exists():

                print(
                    f"Invalid image {scene_number}. "
                    f"Regenerating..."
                )

                image_path.unlink()

            else:

                print(
                    f"Generating image {scene_number}..."
                )

            image_generator.generate(
                scene=scene,
                output_path=image_path,
            )

        # Voice

        if AssetValidator.is_valid_media(voice_path):

            print(
                f"Skipping valid voice {scene_number}"
            )

        else:

            if voice_path.exists():

                print(
                    f"Invalid voice {scene_number}. "
                    f"Regenerating..."
                )

                voice_path.unlink()

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

    run.update_metadata(
        status="images_and_voice_completed"
    )

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
    # ---------------------------------
    # Duration Tracking
    # ---------------------------------

    scene_durations = {}

    for scene, video_path in zip(
        storyboard.scenes,
        video_paths,
    ):

        duration = AssetValidator.get_duration(
            video_path
        )

        scene_durations[
            str(scene.scene_number)
        ] = round(
            duration,
            3
        )

    total_duration = round(
        sum(scene_durations.values()),
        3
    )

    # ---------------------------------
    # Captions
    # ---------------------------------

    print()
    print("Generating captions...")
    print()

    actual_scene_durations = [
        scene_durations[
            str(scene.scene_number)
        ]
        for scene in storyboard.scenes
    ]

    captions_path = (
        run.root / "captions.srt"
    )

    CaptionGenerator.generate_srt(
        scenes=storyboard.scenes,
        scene_durations=actual_scene_durations,
        output_path=captions_path,
    )

    print(
        f"Captions created: {captions_path}"
    )

    run.update_metadata(
        scene_durations=scene_durations,
        total_duration=total_duration,
    )

    run.update_metadata(
        status="scene_videos_completed"
    )

    # ---------------------------------
    # Final Video
    # ---------------------------------

    if AssetValidator.is_valid_video_with_audio(
        run.final_video_path
    ):

        print()
        print(
            "Valid final video already exists. "
            "Skipping concatenation."
        )

    else:

        if run.final_video_path.exists():

            print()
            print(
                "Invalid final video found. "
                "Regenerating..."
            )

            run.final_video_path.unlink()

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


    # ---------------------------------
    # Final Duration Validation
    # ---------------------------------

    final_duration = AssetValidator.get_duration(
        run.final_video_path
    )

    duration_difference = round(
        final_duration - total_duration,
        3
    )

    run.update_metadata(
        status="completed",
        final_video=str(
            run.final_video_path
        ),
        final_duration=round(
            final_duration,
            3
        ),
        total_duration=round(
            total_duration,
            3
        ),
        duration_difference=duration_difference,
    )

    print()
    print(
        f"Scene total duration: "
        f"{total_duration:.3f} seconds"
    )

    print(
        f"Final video duration: "
        f"{final_duration:.3f} seconds"
    )

    print(
        f"Duration difference: "
        f"{duration_difference:.3f} seconds"
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