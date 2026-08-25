import json
from pathlib import Path


def main():

    run = Path(
        "output/20260818_211021_mayas_rainbow_mystery_-_why_does_a_rainbow_appear"
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
    print("RAINBOW YOUTUBE PUBLISHING DRY RUN")
    print("=" * 60)
    print()

    print(
        "Run directory:",
        run,
    )

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

    # ---------------------------------
    # Required asset validation
    # ---------------------------------

    if not video_path.exists():

        raise FileNotFoundError(
            f"Missing video: {video_path}"
        )

    if not captions_path.exists():

        raise FileNotFoundError(
            f"Missing captions: {captions_path}"
        )

    if not thumbnail_path.exists():

        raise FileNotFoundError(
            f"Missing thumbnail: {thumbnail_path}"
        )

    if not metadata_path.exists():

        raise FileNotFoundError(
            f"Missing YouTube metadata: "
            f"{metadata_path}"
        )

    # ---------------------------------
    # File size checks
    # ---------------------------------

    video_size_mb = (
        video_path.stat().st_size
        / (1024 * 1024)
    )

    captions_size_bytes = (
        captions_path.stat().st_size
    )

    thumbnail_size_mb = (
        thumbnail_path.stat().st_size
        / (1024 * 1024)
    )

    metadata_size_bytes = (
        metadata_path.stat().st_size
    )

    print(
        f"Final video size: "
        f"{video_size_mb:.2f} MB"
    )

    print(
        f"Captions size: "
        f"{captions_size_bytes} bytes"
    )

    print(
        f"Thumbnail size: "
        f"{thumbnail_size_mb:.2f} MB"
    )

    print(
        f"Metadata size: "
        f"{metadata_size_bytes} bytes"
    )

    if captions_size_bytes == 0:

        raise ValueError(
            "Captions file is empty."
        )

    if thumbnail_size_mb > 2:

        raise ValueError(
            "Thumbnail exceeds the 2 MB limit."
        )

    # ---------------------------------
    # Load metadata
    # ---------------------------------

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    print()
    print(
        "YouTube title:"
    )

    print(
        metadata.get(
            "title",
            "MISSING",
        )
    )

    print()
    print(
        "Category:"
    )

    print(
        metadata.get(
            "category",
            "MISSING",
        )
    )

    print()
    print(
        "Audience:"
    )

    print(
        metadata.get(
            "audience",
            "MISSING",
        )
    )

    print()

    # ---------------------------------
    # Publishing state
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
    print(
        "Publishing state:"
    )

    print(
        json.dumps(
            state,
            indent=4,
        )
    )

    # ---------------------------------
    # Dry-run result
    # ---------------------------------

    print()
    print("-" * 60)
    print("DRY RUN RESULT")
    print("-" * 60)

    print(
        "Video upload would be:",
        "SKIPPED"
        if state.get("video")
        else "REQUIRED",
    )

    print(
        "Caption upload would be:",
        "SKIPPED"
        if state.get("captions")
        else "REQUIRED",
    )

    print(
        "Thumbnail upload would be:",
        "SKIPPED"
        if state.get("thumbnail")
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