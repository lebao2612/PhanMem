import tempfile
from typing import Optional
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from app.utils import file_util
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
            await file_util.download_to_file(video_url, temp_path)
            return self.upload_video_file(
                access_token=access_token,
                refresh_token=refresh_token,
                file_path=temp_path,
                **meta_kwargs
            )
        finally:
            file_util.delete_file(temp_path)

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

            media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

            request = youtube.videos().insert(
                part="snippet,status",
                body=metadata,
                media_body=media
            )
            response = None
            while response is None:
                _, response = request.next_chunk()

            print(">>> YouTube upload response:", response)

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
            "id": raw.get("id"),
            "title": snippet.get("title", "Untitled"),
            "description": snippet.get("description", ""),
            "tags": [],
            "view_count": int(stats.get("viewCount", 0)) if stats else 0,
            "like_count": int(stats.get("likeCount", 0)) if stats else 0,
            "comment_count": int(stats.get("commentCount", 0)) if stats else 0,
        }
    
    def get_video_stats_list(self, video_ids: list[str], start_date: str, end_date: str, access_token: str, refresh_token: Optional[str] = None) -> list[list]:
        try:
            youtube = self.auth.get_analytics_service(
                access_token=access_token,
                refresh_token=refresh_token
            )
            result = []
            for video_id in video_ids:  
                try:
                    response = youtube.reports().query(
                        ids="channel==MINE",
                        startDate=start_date,
                        endDate=end_date,
                        metrics="views,likes,comments,shares",
                        dimensions="video",
                        filters=f"video=={video_id}"
                    ).execute()
                    rows = response.get("rows", [])
                    if rows:
                        row = rows[0]
                        result.append([
                            video_id,
                            int(row[1]),
                            int(row[2]),
                            int(row[3]),
                            float(row[4])
                        ])

                except HttpError as ve:
                    print(f"[WARN] Không lấy được thống kê cho video {video_id}: {ve}")
                    continue

            return result

        except HttpError as e:
            raise RuntimeError(f"Không thể gọi Analytics API: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định: {e}") from e
