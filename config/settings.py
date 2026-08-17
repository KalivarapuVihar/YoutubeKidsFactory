from dotenv import load_dotenv
from pathlib import Path

import os


load_dotenv()


BASE_DIR = Path(
    __file__
).resolve().parent.parent


# -----------------------------
# Environment Configuration
# -----------------------------

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

YOUTUBE_API_KEY = os.getenv(
    "YOUTUBE_API_KEY"
)

YOUTUBE_CLIENT_ID = os.getenv(
    "YOUTUBE_CLIENT_ID"
)

YOUTUBE_CLIENT_SECRET = os.getenv(
    "YOUTUBE_CLIENT_SECRET"
)

YOUTUBE_GOOGLE_ACCOUNT = os.getenv(
    "YOUTUBE_GOOGLE_ACCOUNT"
)


# -----------------------------
# AI Configuration
# -----------------------------

AI_MODEL = "gpt-5.5"

AI_TEMPERATURE = 0.7

MAX_RETRIES = 3

REQUEST_TIMEOUT = 60

IMAGE_MODEL = "gpt-image-1"

VOICE_MODEL = "gpt-4o-mini-tts"

VOICE_NAME = "alloy"


# -----------------------------
# Project Directories
# -----------------------------

OUTPUT_DIR = (
    BASE_DIR / "output"
)

LESSON_DIR = (
    OUTPUT_DIR / "lessons"
)

IMAGE_DIR = (
    OUTPUT_DIR / "images"
)

VOICE_DIR = (
    OUTPUT_DIR / "voice"
)

VIDEO_DIR = (
    OUTPUT_DIR / "videos"
)


# -----------------------------
# YouTube Configuration
# -----------------------------

YOUTUBE_CREDENTIALS_PATH = (
    BASE_DIR
    / "credentials"
    / "client_secret.json"
)

YOUTUBE_TOKEN_PATH = (
    BASE_DIR
    / "tokens"
    / "youtube_token.json"
)

YOUTUBE_PRIVACY_STATUS = os.getenv(
    "YOUTUBE_PRIVACY_STATUS",
    "private",
)

YOUTUBE_MADE_FOR_KIDS = True

YOUTUBE_LANGUAGE = os.getenv(
    "YOUTUBE_LANGUAGE",
    "en",
)


# -----------------------------
# Video Configuration
# -----------------------------

VIDEO_WIDTH = 1920

VIDEO_HEIGHT = 1080

FPS = 30


# -----------------------------
# Lesson Defaults
# -----------------------------

DEFAULT_LANGUAGE = "English"

DEFAULT_DURATION_MINUTES = 5

DEFAULT_AGE_GROUP = "3-5 Years"