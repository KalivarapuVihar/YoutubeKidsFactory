from pathlib import Path

from utils.asset_validator import AssetValidator


def main():

    mp3 = Path(
        "output/test_voice.mp3"
    )

    mp4 = list(
        Path("output").glob(
            "*/final_video.mp4"
        )
    )

    print(
        "MP3 valid:",
        AssetValidator.is_valid_media(mp3),
    )

    if mp4:

        print(
            "MP4 valid:",
            AssetValidator.is_valid_media(
                mp4[-1]
            ),
        )


if __name__ == "__main__":
    main()