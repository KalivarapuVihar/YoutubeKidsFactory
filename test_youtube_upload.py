from pathlib import Path

from services.youtube_uploader import (
    YouTubeUploader,
)


def main():

    video_path = Path(
        "output/20260810_084916_butterflies/"
        "final_video.mp4"
    )

    uploader = YouTubeUploader(
        credentials_path=Path(
            "credentials/client_secret.json"
        ),
        token_path=Path(
            "tokens/youtube_token.json"
        ),
    )

    print()
    print("=" * 60)
    print("YOUTUBE PRIVATE UPLOAD TEST")
    print("=" * 60)
    print()

    print(
        f"Video: {video_path}"
    )

    print(
        "Privacy: PRIVATE"
    )

    print(
        "Made for Kids: YES"
    )

    print()
    print("Uploading...")
    print()

    result = uploader.upload_video(
        video_path=video_path,
        title=(
            "Butterflies for Kids 🦋 | "
            "Fun Learning Video"
        ),
        description=(
            "Join us for a fun introduction "
            "to butterflies!\n\n"
            "This educational video is designed "
            "for young children and families.\n\n"
            "Learn, explore and discover with "
            "Wonderland Valley."
        ),
        tags=[
            "butterflies for kids",
            "butterfly",
            "kids learning",
            "preschool learning",
            "educational videos for kids",
            "animals for kids",
            "Wonderland Valley",
        ],
        category_id="27",
        privacy_status="private",
        made_for_kids=True,
        language="en",
    )

    print()
    print("=" * 60)
    print("UPLOAD SUCCESSFUL")
    print("=" * 60)
    print()

    print(
        "Video ID:",
        result["video_id"],
    )

    print(
        "YouTube URL:",
        result["url"],
    )

    print(
        "Privacy:",
        result["privacy_status"],
    )

    print(
        "Made for Kids:",
        result["made_for_kids"],
    )

    print()


if __name__ == "__main__":
    main()