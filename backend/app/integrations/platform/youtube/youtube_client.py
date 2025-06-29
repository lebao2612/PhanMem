from googleapiclient.http import MediaFileUpload
from app.exceptions import HandledException
from app.integrations.file import FileClient
from .youtube_auth import YouTubeAuth

class YouTubeClient:
    @staticmethod
    async def upload_video_url(
        refresh_token: str,
        access_token: str,
        video_url: str,
        title: str,
        description: str,
        category: str,
        privacy: str
    ) -> dict:
        temp_path = "upload_video_temp.mp4"

        try:
            await FileClient.download_to_file(video_url, temp_path)

            return YouTubeClient.upload_video_file(
                refresh_token=refresh_token,
                access_token=access_token,
                file_path=temp_path,
                title=title,
                description=description,
                category=category,
                privacy=privacy
            )

        finally:
            FileClient.delete_file(temp_path)

    @staticmethod
    def upload_video_file(
        refresh_token: str,
        access_token: str,
        file_path: str,
        title: str,
        description: str,
        category: str,
        privacy: str
    ) -> dict:
        youtube = YouTubeAuth.get_service(
            refresh_token=refresh_token,
            access_token=access_token
        )

        metadata = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["AI", "video", "upload"],
                "categoryId": category
            },
            "status": {
                "privacyStatus": privacy
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=metadata,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()

        media.stream().close()
        return response


    @staticmethod
    def fetch_video_stats(video_id: str, refresh_token: str, access_token: str) -> dict:
        youtube = YouTubeAuth.get_service(
            refresh_token=refresh_token,
            access_token=access_token
        )
        response = youtube.videos().list(part="statistics", id=video_id).execute()

        items = response.get("items", [])
        if not items:
            raise HandledException(status_code=404, detail="Không tìm thấy video")

        stats = items[0]["statistics"]
        return {
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0))
        }

    @staticmethod
    def get_channel_id(refresh_token: str, access_token: str) -> str:
        youtube = YouTubeAuth.get_service(
            refresh_token=refresh_token,
            access_token=access_token
        )
        response = youtube.channels().list(part="id", mine=True).execute()
        return response["items"][0]["id"]
