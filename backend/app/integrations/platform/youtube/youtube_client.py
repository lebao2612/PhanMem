from googleapiclient.http import MediaFileUpload
from app.exceptions import HandledException
from app.utils import FileUtil
from .youtube_auth import YouTubeAuth

class YouTubeClient:
    @staticmethod
    def trending_videos(region: str = "VN", limit: int = 10) -> list:
        #
        youtube = YouTubeAuth.get_public_service()
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode=region,
            maxResults=limit
        )
        response = request.execute()

        return response["items"]
    
    @staticmethod
    def search_videos(keyword: str, region: str = "VN", limit: int = 10) -> list:
        #
        youtube = YouTubeAuth.get_public_service()
        request = youtube.search().list(
            part="snippet",
            q=keyword,
            type="video",
            maxResults=limit,
            regionCode=region
        )
        response = request.execute()

        return response["items"]

    @staticmethod
    async def upload_video_url(
        refresh_token: str,
        access_token: str,
        video_url: str,
        metadata: dict,
    ) -> dict:
        temp_path = "upload_video_temp.mp4"

        try:
            await FileUtil.download_to_file(video_url, temp_path)

            return YouTubeClient.upload_video_file(
                refresh_token=refresh_token,
                access_token=access_token,
                file_path=temp_path,
                metadata=metadata
            )

        finally:
            FileUtil.delete_file(temp_path)

    @staticmethod
    def upload_video_file(
        refresh_token: str,
        access_token: str,
        file_path: str,
        metadata: dict
    ) -> dict:
        youtube = YouTubeAuth.get_auth_service(
            refresh_token=refresh_token,
            access_token=access_token
        )

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=metadata,
            media_body=media
        )

        response = None
        try:
            while response is None:
                status, response = request.next_chunk()
        except Exception as e:
            raise HandledException(f"Lỗi khi upload video: {e}", 500)

        media.stream().close()
        return response

    @staticmethod
    def get_video_details(video_id: str, refresh_token: str, access_token: str) -> dict:
        youtube = YouTubeAuth.get_auth_service(
            refresh_token=refresh_token,
            access_token=access_token
        )
        request = youtube.videos().list(
            part="snippet,statistics,status,contentDetails",
            id=video_id
        )
        response = request.execute()
        items = response.get("items", [])
        if not items:
            raise HandledException(f"Không tìm thấy video với ID: {video_id}", 404)
        return items[0]

    @staticmethod
    def get_channel_detail(refresh_token: str, access_token: str) -> dict:
        youtube = YouTubeAuth.get_auth_service(
            refresh_token=refresh_token,
            access_token=access_token
        )
        request = youtube.channels().list(
            part="snippet,statistics,status,contentDetails",
            mine=True
        )
        response = request.execute()
        items = response.get("items", [])
        if not items:
            raise HandledException(f"Không tìm thấy channel", 404)
        return items[0]
    
    @staticmethod
    def get_channel_id(refresh_token: str, access_token: str) -> str:
        youtube = YouTubeAuth.get_auth_service(
            refresh_token=refresh_token,
            access_token=access_token
        )

        response = youtube.channels().list(
            part="id",
            mine=True
        ).execute()

        items = response.get("items", [])
        if not items:
            raise HandledException("Không tìm thấy kênh YouTube", 404)

        return items[0]["id"]
