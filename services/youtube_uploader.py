import os
from pathlib import Path
from typing import List

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

        video_path = Path(
            video_path
        )

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

        if (
            privacy_status
            not in allowed_privacy
        ):

            raise ValueError(
                "Invalid privacy status. "
                "Use private, unlisted or public."
            )

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
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
                "https://www.youtube.com/watch?v="
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

            size_mb = (
                file_size / (1024 * 1024)
            )

            raise ValueError(
                "Thumbnail is too large: "
                f"{size_mb:.2f} MB. "
                "YouTube requires thumbnails "
                "to be 2 MB or smaller."
            )

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

        body = {
            "id": video_id,
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
                "defaultLanguage": language,
                "defaultAudioLanguage": language,
            },
            "status": {
                "selfDeclaredMadeForKids": made_for_kids,
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