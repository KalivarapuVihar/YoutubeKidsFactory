from pathlib import Path

from config.settings import (
    YOUTUBE_CREDENTIALS_PATH,
    YOUTUBE_TOKEN_PATH,
)
from services.youtube_uploader import YouTubeUploader


VIDEO_ID = "h8KjETBgIYc"

METADATA = {
    "title": "Maya's Rainbow Mystery | Preschool Science & Colors for Kids",

    "description": """Join Maya in Wonderland Valley as she solves a colorful mystery: where do rainbows come from?

In this gentle preschool science adventure, children discover that rainbows can appear when sunlight shines through tiny drops of water in the air.

Kids will explore rainbows after rain, colorful water mist, and simple examples of how sunlight and water create rainbow colors. The episode also supports color recognition through red, orange, yellow, green, blue, and purple.

Perfect for children ages 2–6 who enjoy gentle learning about colors, weather, nature, and simple science.

#PreschoolScience #RainbowsForKids #LearnColors #KidsLearning #WonderlandValley""",

    "tags": [
        "Wonderland Valley",
        "Maya's Rainbow Mystery",
        "rainbows for kids",
        "preschool science",
        "colors for kids",
        "learn colors",
        "rainbow colors",
        "weather for preschoolers",
        "science for toddlers",
        "science for preschoolers",
        "kids educational animation",
        "preschool learning video",
        "simple science for kids",
        "rainbow lesson for kids",
        "sunlight and water",
        "color recognition",
        "toddler learning",
        "kindergarten science",
        "educational videos for kids",
        "Maya rainbow song",
    ],
}


def main():
    print("=" * 60)
    print("UPDATING EXISTING YOUTUBE VIDEO")
    print("=" * 60)
    print()
    print("Video ID:", VIDEO_ID)
    print("Privacy: PRIVATE")
    print()

    uploader = YouTubeUploader(
        credentials_path=YOUTUBE_CREDENTIALS_PATH,
        token_path=YOUTUBE_TOKEN_PATH,
    )

    result = uploader.update_video(
        video_id=VIDEO_ID,
        title=METADATA["title"],
        description=METADATA["description"],
        tags=METADATA["tags"],
        category_id="27",
        privacy_status="private",
        made_for_kids=True,
        language="en",
    )

    print()
    print("=" * 60)
    print("VIDEO METADATA UPDATED")
    print("=" * 60)
    print()
    print("Video ID:", result["video_id"])
    print("Privacy:", result["privacy_status"])
    print("Made for Kids:", result["made_for_kids"])
    print("URL:", result["url"])
    print()


if __name__ == "__main__":
    main()