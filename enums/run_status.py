from enum import Enum


class RunStatus(str, Enum):
    CREATED = "created"
    LESSON_GENERATED = "lesson_generated"
    IMAGE_PROMPTS_GENERATED = "image_prompts_generated"
    IMAGES_GENERATED = "images_generated"
    VOICE_GENERATED = "voice_generated"
    VIDEO_RENDERED = "video_rendered"
    UPLOADED = "uploaded"
    FAILED = "failed"