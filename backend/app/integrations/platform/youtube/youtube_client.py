import tempfile
from typing import Optional
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from app.utils import FileIOUtil
from .youtube_auth import YouTubeAuth


class YouTubeClient:
    def __init__(self, auth: YouTubeAuth):
        self.auth = auth

    def trending_videos(self, region: str = "VN", limit: int = 10) -> list:
        youtube = self.auth.get_public_service()
        try:
            request = youtube.videos().list(
                part="snippet",
                chart="mostPopular",
                regionCode=region,
                maxResults=limit
            )
            response = request.execute()
            return [self.normalize_youtube_video_data(item) for item in response.get("items", [])]
        except Exception as e:
            raise RuntimeError(f"Không thể truy cập danh sách video trending từ YouTube: {e}.") from e

    def fetch_search_results(self, keyword: str, region: str = "VN", limit: int = 10) -> list:
        youtube = self.auth.get_public_service()
        try:
            request = youtube.search().list(
                part="snippet",
                q=keyword,
                type="video",
                maxResults=limit,
                regionCode=region
            )
            response = request.execute()
            return [self.normalize_youtube_video_data(item) for item in response.get("items", [])]
        except Exception as e:
            raise RuntimeError(f"Không thể tìm kiếm video từ YouTube: {e}") from e

    async def upload_video_url(
        self,
        access_token: str,
        video_url: str,
        refresh_token: Optional[str] = None,
        **meta_kwargs
    ) -> dict:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
            temp_path = tmp_file.name

        try:
            await FileIOUtil.download_to_file(video_url, temp_path)
            return self.upload_video_file(
                access_token=access_token,
                refresh_token=refresh_token,
                file_path=temp_path,
                **meta_kwargs
            )
        finally:
            FileIOUtil.delete_file(temp_path)

    def upload_video_file(
        self,
        access_token: str,
        file_path: str,
        refresh_token: Optional[str] = None,
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
            youtube = self.auth.get_auth_service(access_token=access_token, refresh_token=refresh_token)

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
            return self.normalize_youtube_video_data(response)

        except HttpError as e:
            if e.resp.status == 403:
                raise PermissionError("Không đủ quyền để upload video.") from e
            elif e.resp.status == 401:
                raise PermissionError("Token không hợp lệ hoặc đã hết hạn.") from e
            raise RuntimeError("Lỗi khi upload video lên YouTube.") from e
        except Exception as e:
            raise RuntimeError("Lỗi không xác định khi upload video.") from e

    def get_video_details(self, video_id: str, access_token: str, refresh_token: Optional[str] = None) -> dict:
        try:
            youtube = self.auth.get_auth_service(access_token=access_token, refresh_token=refresh_token)
            request = youtube.videos().list(
                part="snippet,statistics,status,contentDetails",
                id=video_id
            )
            response = request.execute()
            items = response.get("items", [])
            if not items:
                raise ValueError(f"Không tìm thấy video với ID: {video_id}")
            return self.normalize_youtube_video_data(items[0])
        except HttpError as e:
            raise RuntimeError("Không thể lấy thông tin video.") from e
        except Exception as e:
            raise RuntimeError("Lỗi không xác định khi lấy video detail.") from e

    def get_channel_detail(self, access_token: str, refresh_token: Optional[str] = None) -> dict:
        try:
            youtube = self.auth.get_auth_service(access_token=access_token, refresh_token=refresh_token)
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

    def normalize_youtube_video_data(self, raw: dict) -> dict:
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
