from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")

YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

# -----------------------------
# AI Configuration
# -----------------------------

AI_MODEL = "gpt-5.5"

AI_TEMPERATURE = 0.7

MAX_RETRIES = 3

REQUEST_TIMEOUT = 60

# -----------------------------
# Project Directories
# -----------------------------

OUTPUT_DIR = "output"

IMAGE_DIR = "output/images"

VOICE_DIR = "output/voice"

VIDEO_DIR = "output/video"

LESSON_DIR = "output/lessons"

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