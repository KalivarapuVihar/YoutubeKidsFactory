import json
from pathlib import Path


def main():

    run = Path(
        "output/20260810_084916_butterflies"
    )

    video_path = (
        run / "final_video.mp4"
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

    result_path = (
        run / "youtube_result.json"
    )

    print()
    print("=" * 60)
    print("YOUTUBE PUBLISHING DRY RUN")
    print("=" * 60)
    print()

    print(
        "Final video:",
        video_path.exists(),
    )

    print(
        "Captions:",
        captions_path.exists(),
    )

    print(
        "Thumbnail:",
        thumbnail_path.exists(),
    )

    print(
        "Metadata:",
        metadata_path.exists(),
    )

    print()

    if not video_path.exists():
        raise FileNotFoundError(
            f"Missing video: {video_path}"
        )

    if not captions_path.exists():
        raise FileNotFoundError(
            f"Missing captions: {captions_path}"
        )

    if not thumbnail_path.exists():
        print(
            "WARNING: Thumbnail does not exist yet."
        )

    if not metadata_path.exists():
        print(
            "WARNING: YouTube metadata does not exist."
        )

    # ---------------------------------
    # Simulate publishing state
    # ---------------------------------

    if result_path.exists():

        state = json.loads(
            result_path.read_text(
                encoding="utf-8"
            )
        )

        print(
            "Existing publishing state found."
        )

    else:

        state = {
            "video": None,
            "captions": None,
            "thumbnail": None,
        }

        print(
            "No publishing state found."
        )

    print()
    print("Publishing state:")
    print(
        json.dumps(
            state,
            indent=4,
        )
    )

    print()
    print("-" * 60)
    print("DRY RUN RESULT")
    print("-" * 60)

    print(
        "Video upload would be:",
        "SKIPPED"
        if state["video"]
        else "REQUIRED",
    )

    print(
        "Caption upload would be:",
        "SKIPPED"
        if state["captions"]
        else "REQUIRED",
    )

    print(
        "Thumbnail upload would be:",
        "SKIPPED"
        if state["thumbnail"]
        else "REQUIRED",
    )

    print()
    print(
        "NO YouTube API upload was performed."
    )
    print(
        "NO OpenAI API request was performed."
    )
    print()


if __name__ == "__main__":
    main()