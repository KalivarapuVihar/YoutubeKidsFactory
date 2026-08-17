from pathlib import Path

from services.youtube_uploader import (
    YouTubeUploader,
)


def main():

    video_id = "p0AhFmNvEac"

    thumbnail_path = Path(
        "output/test_thumbnail.jpg"
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
    print("YOUTUBE THUMBNAIL UPLOAD TEST")
    print("=" * 60)
    print()

    print(
        "Video ID:",
        video_id,
    )

    print(
        "Thumbnail:",
        thumbnail_path,
    )

    print()
    print("Uploading thumbnail...")
    print()

    result = uploader.set_thumbnail(
        video_id=video_id,
        thumbnail_path=thumbnail_path,
    )

    print()
    print("=" * 60)
    print("THUMBNAIL UPLOAD SUCCESSFUL")
    print("=" * 60)
    print()

    print(
        "Video ID:",
        result["video_id"],
    )

    print(
        "Thumbnail uploaded:",
        result["thumbnail_uploaded"],
    )


if __name__ == "__main__":
    main()