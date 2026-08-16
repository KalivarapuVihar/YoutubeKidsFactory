from pathlib import Path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class YouTubeUploader:

    SCOPES = [
        "https://www.googleapis.com/auth/youtube.upload"
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

        self.youtube = self._authenticate()

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

                credentials.refresh(
                    Request()
                )

        if not credentials or not credentials.valid:

            flow = (
                InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path),
                    self.SCOPES,
                )
            )

            credentials = flow.run_local_server(
                port=0
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
                f"Video not found: {video_path}"
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
                "selfDeclaredMadeForKids": made_for_kids,
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

            _, response = request.next_chunk()

        video_id = response["id"]

        return {
            "video_id": video_id,
            "url": (
                f"https://www.youtube.com/watch?v="
                f"{video_id}"
            ),
            "privacy_status": privacy_status,
            "made_for_kids": made_for_kids,
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

        media = MediaFileUpload(
            str(thumbnail_path),
            mimetype="image/png",
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