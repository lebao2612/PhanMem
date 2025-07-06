import tempfile
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from app.utils import FileUtil
from .youtube_auth import YouTubeAuth


class YouTubeClient:
    @staticmethod
    def trending_videos(region: str = "VN", limit: int = 10) -> list:
        youtube = YouTubeAuth.get_public_service()
        try:
            request = youtube.videos().list(
                part="snippet",
                chart="mostPopular",
                regionCode=region,
                maxResults=limit
            )
            response = request.execute()
            items = response.get("items", [])
            return [YouTubeClient.normalize_youtube_video_data(item) for item in items]
        except HttpError as e:
            raise RuntimeError("Không thể truy cập danh sách video trending từ YouTube.") from e

    @staticmethod
    def fetch_search_results(keyword: str, region: str = "VN", limit: int = 10) -> list:
        youtube = YouTubeAuth.get_public_service()
        try:
            request = youtube.search().list(
                part="snippet",
                q=keyword,
                type="video",
                maxResults=limit,
                regionCode=region
            )
            response = request.execute()
            items = response.get("items", [])
            return [YouTubeClient.normalize_youtube_video_data(item) for item in items]
        except HttpError as e:
            raise RuntimeError("Không thể tìm kiếm video từ YouTube.") from e

    @staticmethod
    async def upload_video_url(
        access_token: str,
        video_url: str,
        refresh_token: str = None,
        **meta_kwargs
    ) -> dict:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            temp_path = tmp_file.name

        try:
            await FileUtil.download_to_file(video_url, temp_path)
            return YouTubeClient.upload_video_file(
                refresh_token=refresh_token,
                access_token=access_token,
                file_path=temp_path,
                meta_kwargs=meta_kwargs
            )
        finally:
            FileUtil.delete_file(temp_path)

    @staticmethod
    def upload_video_file(
        access_token: str,
        file_path: str,
        refresh_token: str = None,
        **meta_kwargs
    ) -> dict:
        metadata = {
            "snippet": {
                "title": meta_kwargs.get("title", "Untitled"),
                "description": meta_kwargs.get("description", ""),
                "categoryId": meta_kwargs.get("categoryId", "22"),
                "tags": meta_kwargs.get("tags", []),
                "defaultLanguage": "vi"
            },
            "status": {
                "privacyStatus": meta_kwargs.get("privacy", "private")
            }
        }

        try:
            youtube = YouTubeAuth.get_auth_service(
                refresh_token=refresh_token,
                access_token=access_token
            )

            with MediaFileUpload(file_path, chunksize=-1, resumable=True) as media:
                request = youtube.videos().insert(
                    part="snippet,status",
                    body=metadata,
                    media_body=media
                )
                response = None
                while response is None:
                    _, response = request.next_chunk()

            media.stream().close()
            return YouTubeClient.normalize_youtube_video_data(response)

        except HttpError as e:
            if e.resp.status == 403:
                raise PermissionError("Không đủ quyền để upload video.") from e
            elif e.resp.status == 401:
                raise PermissionError("Token không hợp lệ hoặc đã hết hạn.") from e
            raise RuntimeError("Lỗi khi upload video lên YouTube.") from e
        except Exception as e:
            raise RuntimeError("Lỗi không xác định khi upload video.") from e

    @staticmethod
    def get_video_details(video_id: str, access_token: str, refresh_token: str = None) -> dict:
        try:
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
                raise ValueError(f"Không tìm thấy video với ID: {video_id}")
            return YouTubeClient.normalize_youtube_video_data(items[0])
        except HttpError as e:
            raise RuntimeError("Không thể lấy thông tin video.") from e
        except Exception as e:
            raise RuntimeError("Lỗi không xác định khi lấy video detail.") from e

    @staticmethod
    def get_channel_detail(access_token: str, refresh_token: str = None) -> dict:
        try:
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
                raise ValueError("Không tìm thấy channel")
            return items[0]
        except HttpError as e:
            raise RuntimeError("Không thể lấy thông tin channel.") from e
        except Exception as e:
            raise RuntimeError("Lỗi không xác định khi lấy thông tin channel.") from e

    @staticmethod
    def normalize_youtube_video_data(raw: dict) -> dict:
        snippet = raw.get("snippet", {})
        status = raw.get("status", {})
        stats = raw.get("statistics", {})

        return {
            "id": raw.get("id") or raw.get("id", {}).get("videoId"),
            "title": snippet.get("title", "Untitled"),
            "description": snippet.get("description", ""),
            "tags": snippet.get("tags", []),
            "view_count": int(stats.get("viewCount", 0)) if stats else 0,
            "like_count": int(stats.get("likeCount", 0)) if stats else 0,
            "comment_count": int(stats.get("commentCount", 0)) if stats else 0,
        }
