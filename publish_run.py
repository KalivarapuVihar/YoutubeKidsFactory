import json
import subprocess
from pathlib import Path

from config.settings import (
    YOUTUBE_CREDENTIALS_PATH,
    YOUTUBE_TOKEN_PATH,
    YOUTUBE_PRIVACY_STATUS,
    YOUTUBE_MADE_FOR_KIDS,
    YOUTUBE_LANGUAGE,
)
from models.storyboard import Storyboard
from services.youtube_uploader import YouTubeUploader
from utils.asset_validator import AssetValidator
from utils.caption_generator import CaptionGenerator


RUN_DIRECTORY = Path(
    "output/20260818_222639_mayas_rainbow_mystery"
)


def load_json(path: Path) -> dict:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def save_json(path: Path, data: dict) -> None:
    path.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def validate_final_video(video_path: Path) -> None:
    if not video_path.exists():
        raise FileNotFoundError(
            f"Final video not found: {video_path}"
        )

    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_name,width,height,pix_fmt",
        "-of",
        "json",
        str(video_path),
    ]

    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    streams = json.loads(result.stdout).get(
        "streams",
        []
    )

    if not streams:
        raise ValueError(
            "Final video has no video stream."
        )

    stream = streams[0]

    if stream.get("codec_name") != "h264":
        raise ValueError(
            "Final video must use H.264."
        )

    if (
        stream.get("width") != 1280
        or stream.get("height") != 720
    ):
        raise ValueError(
            "Final video must be 1280x720."
        )

    if stream.get("pix_fmt") != "yuv420p":
        raise ValueError(
            "Final video must use yuv420p."
        )


def generate_captions(
    run: Path,
) -> Path:

    storyboard_path = (
        run / "storyboard.json"
    )

    captions_path = (
        run / "captions.srt"
    )

    storyboard = Storyboard.model_validate(
        load_json(storyboard_path)
    )

    scene_durations = []

    for scene in storyboard.scenes:

        video_path = (
            run
            / "video"
            / f"scene_{scene.scene_number:02d}.mp4"
        )

        if not video_path.exists():
            raise FileNotFoundError(
                f"Scene video not found: "
                f"{video_path}"
            )

        duration = (
            AssetValidator.get_duration(
                video_path
            )
        )

        scene_durations.append(
            duration
        )

    CaptionGenerator.generate_srt(
        storyboard.scenes,
        scene_durations,
        captions_path,
    )

    if (
        not captions_path.exists()
        or captions_path.stat().st_size == 0
    ):
        raise ValueError(
            "Caption generation produced an empty file."
        )

    return captions_path


def validate_thumbnail(
    thumbnail_path: Path,
) -> None:

    if not thumbnail_path.exists():
        raise FileNotFoundError(
            f"Thumbnail not found: {thumbnail_path}"
        )

    max_size = 2 * 1024 * 1024

    if thumbnail_path.stat().st_size > max_size:
        raise ValueError(
            "Thumbnail exceeds YouTube's 2 MB limit."
        )

    if (
        thumbnail_path.suffix.lower()
        not in {".jpg", ".jpeg", ".png"}
    ):
        raise ValueError(
            "Thumbnail must be JPG, JPEG, or PNG."
        )


def load_publishing_state(
    result_path: Path,
) -> dict:

    if not result_path.exists():
        return {
            "video": None,
            "captions": None,
            "thumbnail": None,
        }

    state = load_json(result_path)

    # Backward compatibility with an older
    # publishing-state key.
    if (
        state.get("captions") is None
        and state.get("caption") is not None
    ):
        state["captions"] = state["caption"]

    state.setdefault("video", None)
    state.setdefault("captions", None)
    state.setdefault("thumbnail", None)

    return state


def preflight(
    run: Path,
) -> dict:

    video_path = (
        run / "final_motion_video.mp4"
    )

    captions_path = (
        run / "captions.srt"
    )

    thumbnail_path = (
        run / "thumbnail.jpg"
    )

    metadata_path = (
        run / "youtube_metadata.json"
    )

    print()
    print("=" * 60)
    print("YOUTUBE PUBLISHING PREFLIGHT")
    print("=" * 60)
    print()

    print(
        "Run directory:",
        run,
    )

    validate_final_video(
        video_path
    )

    print(
        "Final video: OK (1280x720 H.264)"
    )

    print(
        "Generating captions from actual scene durations..."
    )

    generate_captions(run)

    print(
        "Captions: OK"
    )

    if not metadata_path.exists():
        raise FileNotFoundError(
            "YouTube metadata does not exist: "
            f"{metadata_path}"
        )

    metadata = load_json(
        metadata_path
    )

    required_metadata = [
        "title",
        "description",
        "tags",
        "category",
    ]

    missing = [
        key
        for key in required_metadata
        if key not in metadata
    ]

    if missing:
        raise ValueError(
            "YouTube metadata is missing fields: "
            + ", ".join(missing)
        )

    print(
        "Metadata: OK"
    )

    validate_thumbnail(
        thumbnail_path
    )

    print(
        "Thumbnail: OK"
    )

    print()
    print(
        "Title:",
        metadata["title"],
    )

    print(
        "Category:",
        metadata["category"],
    )

    print(
        "Privacy:",
        YOUTUBE_PRIVACY_STATUS,
    )

    print(
        "Made for Kids:",
        YOUTUBE_MADE_FOR_KIDS,
    )

    if YOUTUBE_PRIVACY_STATUS != "private":
        raise ValueError(
            "Publishing stopped: "
            "YOUTUBE_PRIVACY_STATUS must be 'private' "
            "for this first upload."
        )

    if YOUTUBE_MADE_FOR_KIDS is not True:
        raise ValueError(
            "Publishing stopped: "
            "YOUTUBE_MADE_FOR_KIDS must be True."
        )

    return {
        "video_path": video_path,
        "captions_path": captions_path,
        "thumbnail_path": thumbnail_path,
        "metadata_path": metadata_path,
        "metadata": metadata,
    }


def main():

    run = RUN_DIRECTORY

    if not run.exists():
        raise FileNotFoundError(
            f"Run directory not found: {run}"
        )

    assets = preflight(run)

    result_path = (
        run / "youtube_result.json"
    )

    state = load_publishing_state(
        result_path
    )

    print()
    print(
        "Existing publishing state:"
    )
    print(
        json.dumps(
            state,
            indent=4,
        )
    )

    print()
    print("=" * 60)
    print("STARTING YOUTUBE PUBLISH")
    print("=" * 60)
    print()

    uploader = YouTubeUploader(
        credentials_path=(
            YOUTUBE_CREDENTIALS_PATH
        ),
        token_path=(
            YOUTUBE_TOKEN_PATH
        ),
    )

    metadata = assets["metadata"]

    # ---------------------------------
    # Video
    # ---------------------------------

    if state["video"]:

        video_id = state["video"]["video_id"]

        print(
            "Video already uploaded."
        )
        print(
            "Skipping video upload:",
            video_id,
        )

    else:

        print(
            "Uploading video as PRIVATE..."
        )

        state["video"] = (
            uploader.upload_video(
                video_path=(
                    assets["video_path"]
                ),
                title=metadata["title"],
                description=(
                    metadata["description"]
                    + "\n\n"
                    + " ".join(metadata.get("hashtags", []))
                ),
                tags=metadata["tags"],
                category_id="27",
                privacy_status=(
                    YOUTUBE_PRIVACY_STATUS
                ),
                made_for_kids=(
                    YOUTUBE_MADE_FOR_KIDS
                ),
                language=(
                    YOUTUBE_LANGUAGE
                ),
            )
        )

        save_json(
            result_path,
            state,
        )

        print(
            "Video upload successful."
        )

    video_id = state["video"]["video_id"]

    # ---------------------------------
    # Captions
    # ---------------------------------

    if state["captions"]:

        print(
            "Captions already uploaded."
        )
        print(
            "Skipping caption upload."
        )

    else:

        print(
            "Uploading English captions..."
        )

        state["captions"] = (
            uploader.upload_captions(
                video_id=video_id,
                caption_path=(
                    assets["captions_path"]
                ),
                language=(
                    YOUTUBE_LANGUAGE
                ),
                name="English",
                is_draft=False,
            )
        )

        save_json(
            result_path,
            state,
        )

        print(
            "Caption upload successful."
        )

    # ---------------------------------
    # Thumbnail
    # ---------------------------------

    if state["thumbnail"]:

        print(
            "Thumbnail already uploaded."
        )
        print(
            "Skipping thumbnail upload."
        )

    else:

        print(
            "Uploading thumbnail..."
        )

        state["thumbnail"] = (
            uploader.set_thumbnail(
                video_id=video_id,
                thumbnail_path=(
                    assets["thumbnail_path"]
                ),
            )
        )

        save_json(
            result_path,
            state,
        )

        print(
            "Thumbnail upload successful."
        )

    # ---------------------------------
    # Completion
    # ---------------------------------

    state["status"] = "uploaded_private"
    state["video_id"] = video_id
    state["url"] = (
        state["video"]["url"]
    )
    state["privacy_status"] = (
        YOUTUBE_PRIVACY_STATUS
    )
    state["made_for_kids"] = (
        YOUTUBE_MADE_FOR_KIDS
    )

    save_json(
        result_path,
        state,
    )

    print()
    print("=" * 60)
    print("YOUTUBE UPLOAD SUCCESSFUL")
    print("=" * 60)
    print()

    print(
        "Video ID:",
        video_id,
    )

    print(
        "URL:",
        state["url"],
    )

    print(
        "Privacy:",
        state["privacy_status"],
    )

    print(
        "Made for Kids:",
        state["made_for_kids"],
    )

    print()
    print("Upload state saved to:", result_path)
    print("Video remains PRIVATE. Make it PUBLIC manually in YouTube Studio.")
    
    print()


if __name__ == "__main__":
    main()
