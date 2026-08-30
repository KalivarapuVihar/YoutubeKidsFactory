import os
from pathlib import Path
from typing import List
import subprocess
from utils.logger import logger
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class YouTubeUploader:

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
    ]

    def __init__(
        self,
        credentials_path: Path,
        token_path: Path,
    ):

        self.credentials_path = Path(
            credentials_path
        )

        self.token_path = Path(
            token_path
        )

        self.youtube = (
            self._authenticate()
        )

    def _authenticate(self):

        credentials = None

        if self.token_path.exists():

            credentials = (
                Credentials.from_authorized_user_file(
                    str(self.token_path),
                    self.SCOPES,
                )
            )

        if credentials and credentials.expired:
            if credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except Exception as exc:
                    print()
                    print("Existing YouTube token could not be refreshed.")
                    print("A new YouTube authorization will be requested.")
                    print(f"Reason: {exc}")
                    print()
                    credentials = None

        if (
            not credentials
            or not credentials.valid
        ):

            flow = (
                InstalledAppFlow
                .from_client_secrets_file(
                    str(
                        self.credentials_path
                    ),
                    self.SCOPES,
                )
            )

            credentials = (
                flow.run_local_server(
                    port=0,
                    prompt="consent",
                    login_hint=os.getenv(
                        "YOUTUBE_GOOGLE_ACCOUNT"
                    ),
                )
            )

        self.token_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.token_path,
            "w",
            encoding="utf-8",
        ) as token_file:

            token_file.write(
                credentials.to_json()
            )

        return build(
            "youtube",
            "v3",
            credentials=credentials,
        )

    @staticmethod
    def sanitize_tags(tags: List[str]) -> List[str]:
        """
        Clean and validate YouTube video tags before upload.

        YouTube rejects the entire video metadata request when the
        tags field contains invalid values. Keep tags useful while
        enforcing safe formatting and total length.
        """

        if not tags:
            return []

        cleaned_tags = []
        total_length = 0

        for tag in tags:
            if tag is None:
                continue

            # Convert to string and remove surrounding whitespace.
            tag = str(tag).strip()

            if not tag:
                continue

            # Remove line breaks and control characters.
            tag = " ".join(tag.split())

            # YouTube tags should not contain control characters.
            tag = "".join(
                char
                for char in tag
                if char.isprintable()
            )

            tag = tag.strip()

            if not tag:
                continue

            # Avoid duplicate tags, case-insensitively.
            if any(
                tag.lower() == existing.lower()
                for existing in cleaned_tags
            ):
                continue

            # Individual tags should be reasonably short.
            # Long AI-generated tags provide little additional value.
            if len(tag) > 100:
                tag = tag[:100].rstrip()

            if not tag:
                continue

            # YouTube's tag metadata has a total character limit.
            # Leave room for separators between tags.
            separator_length = (
                1 if cleaned_tags else 0
            )

            if (
                total_length
                + separator_length
                + len(tag)
                > 450
            ):
                logger.warning(
                    "Skipping tag because the safe total "
                    f"tag length limit would be exceeded: {tag!r}"
                )
                continue

            cleaned_tags.append(tag)

            total_length += (
                separator_length + len(tag)
            )

        logger.info(
            f"YouTube tags sanitized: "
            f"{len(tags)} -> {len(cleaned_tags)} tags, "
            f"total length={total_length}"
        )

        return cleaned_tags

    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str],
        category_id: str = "27",
        privacy_status: str = "private",
        made_for_kids: bool = True,
        language: str = "en",
    ) -> dict:

        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(
                f"Video not found: "
                f"{video_path}"
            )

        allowed_privacy = {
            "private",
            "unlisted",
            "public",
        }

        if privacy_status not in allowed_privacy:
            raise ValueError(
                "Invalid privacy status. "
                "Use private, unlisted or public."
            )

        # ---------------------------------
        # Sanitize YouTube tags
        # ---------------------------------

        safe_tags = self.sanitize_tags(tags)

        logger.info(
            f"Uploading video with "
            f"{len(safe_tags)} sanitized tags."
        )

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": safe_tags,
                "categoryId": category_id,
                "defaultLanguage": language,
                "defaultAudioLanguage": language,
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": (
                    made_for_kids
                ),
            },
        }

        media = MediaFileUpload(
            str(video_path),
            mimetype="video/mp4",
            resumable=True,
        )

        request = (
            self.youtube
            .videos()
            .insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )
        )

        response = None

        while response is None:
            _, response = (
                request.next_chunk()
            )

        video_id = response["id"]

        return {
            "video_id": video_id,
            "url": (
            "[https://www.youtube.com/watch?v=](https://www.youtube.com/watch?v=)"
            f"{video_id}"
            ),
            "privacy_status": (
                privacy_status
            ),
            "made_for_kids": (
                made_for_kids
            ),
        }

    def upload_captions(
        self,
        video_id: str,
        caption_path: Path,
        language: str = "en",
        name: str = "English",
        is_draft: bool = False,
    ) -> dict:

        caption_path = Path(
            caption_path
        )

        if not caption_path.exists():

            raise FileNotFoundError(
                f"Caption file not found: "
                f"{caption_path}"
            )

        body = {
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": name,
                "isDraft": is_draft,
            }
        }

        media = MediaFileUpload(
            str(caption_path),
            mimetype="application/octet-stream",
            resumable=False,
        )

        response = (
            self.youtube
            .captions()
            .insert(
                part="snippet",
                body=body,
                media_body=media,
            )
            .execute()
        )

        return {
            "caption_id": response["id"],
            "language": language,
            "name": name,
        }

    def set_thumbnail(
        self,
        video_id: str,
        thumbnail_path: Path,
    ) -> dict:

        thumbnail_path = Path(
            thumbnail_path
        )

        if not thumbnail_path.exists():

            raise FileNotFoundError(
                f"Thumbnail not found: "
                f"{thumbnail_path}"
            )

        max_size = 2 * 1024 * 1024
        file_size = thumbnail_path.stat().st_size

        if file_size > max_size:
            logger.warning(
                f"Thumbnail is too large "
                f"({file_size / (1024 * 1024):.2f} MB). "
                "Compressing automatically..."
            )

            compressed_path = (
                thumbnail_path.parent
                / f"{thumbnail_path.stem}_compressed.jpg"
            )

            compress_command = [
                "ffmpeg",
                "-y",
                "-i",
                str(thumbnail_path),
                "-q:v",
                "8",
                "-frames:v",
                "1",
                str(compressed_path),
            ]

            try:
                subprocess.run(
                    compress_command,
                    check=True,
                    capture_output=True,
                    text=True,
                )

            except subprocess.CalledProcessError as error:
                logger.error(
                    "Thumbnail compression failed."
                )
                logger.error(error.stderr)
                raise

            compressed_size = (
                compressed_path.stat().st_size
            )

            # If quality 8 is still too large,
            # progressively increase JPEG compression.
            quality = 10

            while (
                compressed_size > max_size
                and quality <= 20
            ):
                logger.warning(
                    f"Compressed thumbnail is still too large "
                    f"({compressed_size / (1024 * 1024):.2f} MB). "
                    f"Retrying with quality {quality}."
                )

                compress_command = [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(thumbnail_path),
                    "-q:v",
                    str(quality),
                    "-frames:v",
                    "1",
                    str(compressed_path),
                ]

                subprocess.run(
                    compress_command,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                compressed_size = (
                    compressed_path.stat().st_size
                )

                quality += 2

            if compressed_size > max_size:
                raise ValueError(
                    "Unable to compress thumbnail "
                    "below YouTube's 2 MB limit."
                )

            logger.info(
                f"Thumbnail compressed successfully: "
                f"{compressed_size / (1024 * 1024):.2f} MB"
            )

            thumbnail_path = compressed_path

        extension = (
            thumbnail_path
            .suffix
            .lower()
        )

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
        }

        if extension not in mime_types:

            raise ValueError(
                "Unsupported thumbnail format. "
                "Use JPG, JPEG, or PNG."
            )

        media = MediaFileUpload(
            str(thumbnail_path),
            mimetype=mime_types[
                extension
            ],
            resumable=False,
        )

        response = (
            self.youtube
            .thumbnails()
            .set(
                videoId=video_id,
                media_body=media,
            )
            .execute()
        )

        return {
            "thumbnail_uploaded": True,
            "video_id": video_id,
        }
    
    def update_video(
        self,
        video_id: str,
        title: str,
        description: str,
        tags: List[str],
        category_id: str = "27",
        made_for_kids: bool = True,
        language: str = "en",
    ) -> dict:

        # ---------------------------------
        # Sanitize YouTube tags
        # ---------------------------------

        cleaned_tags = []

        for tag in tags or []:

            if tag is None:
                continue

            tag = str(tag).strip()

            if not tag:
                continue

            # Remove line breaks and tabs.
            tag = (
                tag.replace("\n", " ")
                .replace("\r", " ")
                .replace("\t", " ")
            )

            # Collapse repeated whitespace.
            tag = " ".join(
                tag.split()
            )

            if not tag:
                continue

            # YouTube tags must be reasonably sized.
            # Ignore excessively long individual tags.
            if len(tag) > 500:
                continue

            if tag not in cleaned_tags:
                cleaned_tags.append(tag)

        # YouTube's tag metadata has a total character
        # limit. Keep a safe margin below the limit.
        MAX_TAG_CHARACTERS = 450

        final_tags = []
        total_tag_characters = 0

        for tag in cleaned_tags:

            # YouTube counts spaces between tags too.
            separator_length = (
                1 if final_tags else 0
            )

            required_length = (
                separator_length
                + len(tag)
            )

            if (
                total_tag_characters
                + required_length
                > MAX_TAG_CHARACTERS
            ):
                break

            final_tags.append(tag)

            total_tag_characters += (
                required_length
            )

        print()
        print(
            "YouTube tags prepared:"
        )

        for index, tag in enumerate(
            final_tags,
            start=1,
        ):
            print(
                f"  {index}. {tag}"
            )

        print(
            f"Total tag characters: "
            f"{total_tag_characters}"
        )
        print()

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": final_tags,
                "categoryId": category_id,
                "defaultLanguage": language,
                "defaultAudioLanguage": language,
            },
        }

        response = (
            self.youtube
            .videos()
            .update(
                part="snippet,status",
                body=body,
            )
            .execute()
        )

        return {
            "video_id": response["id"],
            "url": (
                "https://www.youtube.com/watch?v="
                + response["id"]
            ),
            "privacy_status": response["status"].get(
                              "privacyStatus"
            ),
            "made_for_kids": response["status"].get(
                "selfDeclaredMadeForKids"
            ),
        }