from pathlib import Path

from services.youtube_uploader import (
    YouTubeUploader,
)


def main():

    video_id = "p0AhFmNvEac"

    uploader = YouTubeUploader(
        credentials_path=Path(
            "credentials/client_secret.json"
        ),
        token_path=Path(
            "tokens/youtube_token.json"
        ),
    )

    response = (
        uploader.youtube
        .captions()
        .list(
            part="snippet",
            videoId=video_id,
        )
        .execute()
    )

    items = response.get(
        "items",
        [],
    )

    print()
    print("=" * 60)
    print("YOUTUBE CAPTION STATUS")
    print("=" * 60)
    print()

    if not items:

        print(
            "No caption tracks found."
        )

        return

    for item in items:

        snippet = item.get(
            "snippet",
            {},
        )

        print(
            "Caption ID:",
            item.get("id"),
        )

        print(
            "Language:",
            snippet.get("language"),
        )

        print(
            "Name:",
            snippet.get("name"),
        )

        print(
            "Draft:",
            snippet.get("isDraft"),
        )

        print(
            "Status:",
            snippet.get("status"),
        )

        print(
            "Failure reason:",
            snippet.get(
                "failureReason",
                "None",
            ),
        )

        print()


if __name__ == "__main__":
    main()