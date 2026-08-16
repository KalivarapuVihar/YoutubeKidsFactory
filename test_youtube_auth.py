from pathlib import Path

from services.youtube_uploader import (
    YouTubeUploader,
)


def main():

    uploader = YouTubeUploader(
        credentials_path=Path(
            "credentials/client_secret.json"
        ),
        token_path=Path(
            "tokens/youtube_token.json"
        ),
    )

    response = (
        uploader.youtube.channels()
        .list(
            part="snippet",
            mine=True,
        )
        .execute()
    )

    print()
    print("=" * 60)
    print("YOUTUBE AUTHENTICATION SUCCESSFUL")
    print("=" * 60)
    print()

    items = response.get(
        "items",
        [],
    )

    if not items:

        print(
            "Authentication worked, but no "
            "YouTube channel was returned."
        )

        return

    channel = items[0]

    print(
        "Channel:",
        channel["snippet"]["title"],
    )

    print()
    print(
        "YouTube OAuth test passed."
    )


if __name__ == "__main__":
    main()