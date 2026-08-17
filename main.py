from pathlib import Path
from services import youtube_uploader
from services.openai_service import OpenAIService
from services.lesson_generator import LessonGenerator
from services.storyboard_generator import StoryboardGenerator
from services.image_generator import ImageGenerator
from services.voice_generator import VoiceGenerator
from services.video_renderer import VideoRenderer
from services.character_manager import CharacterManager
from utils.caption_generator import CaptionGenerator
from services.youtube_metadata_generator import (
    YouTubeMetadataGenerator,
)
from services.thumbnail_generator import (
    ThumbnailGenerator,
)
from services.youtube_uploader import YouTubeUploader

from config.settings import (
    YOUTUBE_CREDENTIALS_PATH,
    YOUTUBE_TOKEN_PATH,
    YOUTUBE_PRIVACY_STATUS,
    YOUTUBE_MADE_FOR_KIDS,
    YOUTUBE_LANGUAGE,
)

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
        ai_service=ai_service,
        character_manager=character_manager,
    )

    voice_generator = VoiceGenerator(
        ai_service
    )
    youtube_metadata_generator = (
        YouTubeMetadataGenerator(
            ai_service
        )
    )
    thumbnail_generator = ThumbnailGenerator(
        ai_service=ai_service,
        character_manager=character_manager,
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
        status="video_completed",
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

        # ---------------------------------
    # YouTube Metadata
    # ---------------------------------

    print()
    print("Generating YouTube metadata...")
    print()

    if run.youtube_metadata_path.exists():

        print(
            "YouTube metadata already exists. "
            "Skipping generation."
        )

        youtube_metadata_data = (
            FileManager.read_json(
                run.youtube_metadata_path
            )
        )

        from models.youtube_metadata import (
            YouTubeMetadata,
        )

        youtube_metadata = (
            YouTubeMetadata.model_validate(
                youtube_metadata_data
            )
        )

    else:

        youtube_metadata = (
            youtube_metadata_generator.generate(
                topic=lesson.topic,
                introduction=(
                    lesson.introduction
                ),
                examples=lesson.examples,
                activity_description=str(
                    lesson.activity
                ),
                quiz_description=str(
                    lesson.quiz
                ),
                song_title=lesson.song.title,
                song_mood=lesson.song.mood,
                existing_title=(
                    lesson.metadata.title
                ),
                existing_description=(
                    lesson.metadata.description
                ),
                existing_tags=(
                    lesson.metadata.tags
                ),
            )
        )

        FileManager.save_json(
            run.youtube_metadata_path,
            youtube_metadata.model_dump(
                mode="json"
            ),
        )

        print(
            "YouTube metadata generated successfully."
        )

    run.update_metadata(
        status="youtube_metadata_completed"
    )

    print()
    print(
        "YouTube Title:",
        youtube_metadata.title,
    )

    print(
        "YouTube Category:",
        youtube_metadata.category,
    )

    print(
        "YouTube Audience:",
        youtube_metadata.audience,
    )

    # ---------------------------------
    # Thumbnail
    # ---------------------------------

    print()
    print("Preparing YouTube thumbnail...")
    print()

    if run.thumbnail_path.exists():

        print(
            "Thumbnail already exists. "
            "Skipping generation."
        )

    else:

        thumbnail_generator.generate_from_metadata(
            metadata=youtube_metadata,
            output_path=run.thumbnail_path,
        )

        print(
            "Thumbnail generated successfully."
        )

    run.update_metadata(
        status="thumbnail_completed"
    )

    print(
        f"Thumbnail: {run.thumbnail_path}"
    )

    # ---------------------------------
    # YouTube Publishing
    # ---------------------------------

    print()
    print("Preparing YouTube publishing...")
    print()

    # Initialize YouTube only when publishing
    youtube_uploader = YouTubeUploader(
        credentials_path=YOUTUBE_CREDENTIALS_PATH,
        token_path=YOUTUBE_TOKEN_PATH,
    )

    # ---------------------------------
    # Load publishing state
    # ---------------------------------

    if run.youtube_result_path.exists():

        publishing_state = (
            FileManager.read_json(
                run.youtube_result_path
            )
        )

        # Support an older youtube_result.json
        # that contains video information directly.
        if "video_id" in publishing_state:

            publishing_state = {
                "video": publishing_state,
                "captions": None,
                "thumbnail": None,
            }

    else:

        publishing_state = {
            "video": None,
            "captions": None,
            "thumbnail": None,
        }

    # ---------------------------------
    # YouTube Video
    # ---------------------------------

    if publishing_state["video"]:

        youtube_result = (
            publishing_state["video"]
        )

        print(
            "YouTube video already uploaded."
        )

        print(
            "Video ID:",
            youtube_result["video_id"],
        )

    else:

        print(
            "Uploading video to YouTube..."
        )

        youtube_result = (
            youtube_uploader.upload_video(
                video_path=(
                    run.final_video_path
                ),
                title=(
                    youtube_metadata.title
                ),
                description=(
                    youtube_metadata.description
                ),
                tags=(
                    youtube_metadata.tags
                ),
                privacy_status=(
                    YOUTUBE_PRIVACY_STATUS
                ),
                made_for_kids=(
                    YOUTUBE_MADE_FOR_KIDS
                ),
                language=YOUTUBE_LANGUAGE,
            )
        )

        publishing_state["video"] = (
            youtube_result
        )

        # IMPORTANT:
        # Save immediately after video upload.
        # If a later step fails, we never upload
        # another YouTube video on retry.

        FileManager.save_json(
            run.youtube_result_path,
            publishing_state,
        )

        print()
        print(
            "YouTube video uploaded successfully."
        )

        print(
            "Video ID:",
            youtube_result["video_id"],
        )

        print(
            "URL:",
            youtube_result["url"],
        )

    run.update_metadata(
        status="youtube_uploaded",
        youtube_video_id=(
            youtube_result["video_id"]
        ),
        youtube_url=(
            youtube_result["url"]
        ),
        youtube_privacy_status=(
            youtube_result["privacy_status"]
        ),
        youtube_made_for_kids=(
            youtube_result["made_for_kids"]
        ),
    )

    # ---------------------------------
    # YouTube Captions
    # ---------------------------------

    if publishing_state["captions"]:

        caption_result = (
            publishing_state["captions"]
        )

        print()
        print(
            "YouTube captions already uploaded."
        )

    else:

        print()
        print(
            "Uploading YouTube captions..."
        )

        caption_result = (
            youtube_uploader.upload_captions(
                video_id=(
                    youtube_result["video_id"]
                ),
                caption_path=(
                    run.captions_path
                ),
                language=YOUTUBE_LANGUAGE,
                name="English",
                is_draft=False,
            )
        )

        publishing_state["captions"] = (
            caption_result
        )

        # Save immediately.
        FileManager.save_json(
            run.youtube_result_path,
            publishing_state,
        )

        print(
            "YouTube captions uploaded successfully."
        )

    # ---------------------------------
    # YouTube Thumbnail
    # ---------------------------------

    if publishing_state["thumbnail"]:

        thumbnail_result = (
            publishing_state["thumbnail"]
        )

        print()
        print(
            "YouTube thumbnail already uploaded."
        )

    else:

        print()
        print(
            "Uploading YouTube thumbnail..."
        )

        thumbnail_result = (
            youtube_uploader.set_thumbnail(
                video_id=(
                    youtube_result["video_id"]
                ),
                thumbnail_path=(
                    run.thumbnail_path
                ),
            )
        )

        publishing_state["thumbnail"] = (
            thumbnail_result
        )

        # Save immediately.
        FileManager.save_json(
            run.youtube_result_path,
            publishing_state,
        )

        print(
            "YouTube thumbnail uploaded successfully."
        )

    # ---------------------------------
    # Publishing Complete
    # ---------------------------------

    run.update_metadata(
        status="youtube_publishing_completed"
    )

    print()
    print("=" * 50)
    print("YOUTUBE PUBLISHING COMPLETED")
    print("=" * 50)
    print()

    print(
        "Video:",
        youtube_result["url"],
    )

    print(
        "Privacy:",
        youtube_result["privacy_status"],
    )

    print(
        "Made for Kids:",
        youtube_result["made_for_kids"],
    )
    
    # ---------------------------------
    # YouTube Captions
    # ---------------------------------

    print()
    print("Uploading YouTube captions...")
    print()

    caption_result = (
        youtube_uploader.upload_captions(
            video_id=(
                youtube_result["video_id"]
            ),
            caption_path=run.captions_path,
            language=YOUTUBE_LANGUAGE,
            name="English",
            is_draft=False,
        )
    )

    print(
        "YouTube captions uploaded successfully."
    )

    # ---------------------------------
    # YouTube Thumbnail
    # ---------------------------------

    print()
    print("Uploading YouTube thumbnail...")
    print()

    thumbnail_result = (
        youtube_uploader.set_thumbnail(
            video_id=(
                youtube_result["video_id"]
            ),
            thumbnail_path=run.thumbnail_path,
        )
    )

    print(
        "YouTube thumbnail uploaded successfully."
    )

    # ---------------------------------
    # Save YouTube Publishing Results
    # ---------------------------------

    publishing_result = {
        "video": youtube_result,
        "caption": caption_result,
        "thumbnail": thumbnail_result,
    }

    FileManager.save_json(
        run.youtube_result_path,
        publishing_result,
    )

    run.update_metadata(
        status="youtube_publishing_completed"
    )

    print()
    print("=" * 50)
    print("YOUTUBE PUBLISHING COMPLETED")
    print("=" * 50)
    print()

    print(
        "Video:",
        youtube_result["url"],
    )

    print(
        "Privacy:",
        youtube_result["privacy_status"],
    )

    print(
        "Made for Kids:",
        youtube_result["made_for_kids"],
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