import asyncio
from collections import defaultdict
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from app.utils import file_util
from .youtube_auth import YouTubeAuth

class YouTubeClient:
    def __init__(self, auth: YouTubeAuth):
        self.auth = auth

    async def upload_video_url(
        self,
        access_token: str,
        video_url: str,
        refresh_token: str | None = None,
        **meta_kwargs
    ) -> dict:

        try:
            temp_path = await file_util.download_to_tempfile(video_url)
            return await asyncio.to_thread(
                self.upload_video_file,
                access_token=access_token,
                refresh_token=refresh_token,
                file_path=temp_path,
                **meta_kwargs
            )
        finally:
            pass
            # file_util.delete_file(temp_path)

    def upload_video_file(
        self,
        access_token: str,
        file_path: str,
        refresh_token: str | None = None,
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
        media = None
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
            return self._normalize_youtube_video_data(response)
        except HttpError as e:
            if e.resp.status == 403:
                raise PermissionError("Không đủ quyền để upload video.") from e
            elif e.resp.status == 401:
                raise PermissionError("Token không hợp lệ hoặc đã hết hạn") from e
            raise RuntimeError(f"Lỗi khi upload video lên YouTube: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định khi upload video{e}") from e

    def get_video_details(self, video_id: str, access_token: str, refresh_token: str|None = None) -> dict:
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
            return self._normalize_youtube_video_data(items[0])
        except HttpError as e:
            raise RuntimeError("Không thể lấy thông tin video.") from e
        except Exception as e:
            raise RuntimeError("Lỗi không xác định khi lấy video detail.") from e

    def get_channel_detail(self, access_token: str, refresh_token: str|None = None) -> dict:
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

    def _normalize_youtube_video_data(self, raw: dict) -> dict:
        snippet = raw.get("snippet", {})
        status = raw.get("status", {})
        stats = raw.get("statistics", {})

        return {
            "id": raw.get("id"),
            "title": snippet.get("title", "Untitled"),
            "description": snippet.get("description", ""),
            "tags":  snippet.get("tags", []),
            "views": int(stats.get("viewCount", 0)) if stats else 0,
            "likes": int(stats.get("likeCount", 0)) if stats else 0,
            "comments": int(stats.get("commentCount", 0)) if stats else 0,
        }

    async def get_video_statistics(
        self,
        video_ids: list[str],
        access_token: str,
        refresh_token: str | None = None,
    ) -> list[dict]:
        youtube = self.auth.get_auth_service(access_token, refresh_token)
        result = []

        for video_id in video_ids:
            try:
                request = youtube.videos().list(
                    part="snippet,statistics",
                    id=video_id
                )
                response = request.execute()
                items = response.get("items", [])
                if not items:
                    continue
                item = items[0]
                stats = item.get("statistics", {})
                snippet = item.get("snippet", {})
                thumbnails = snippet.get("thumbnails", {})

                result.append({
                    "id": video_id,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "title": snippet.get("title"),
                    "description": snippet.get("description"),
                    "tags": snippet.get("tags", []),
                    "thumbnail": thumbnails.get("high", {}).get("url"),
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "shares": 0  # Không có trong video API
                })
            except HttpError as e:
                print(f"[WARN] Error fetching stats for {video_id}: {e}")
                continue

        return result

    async def get_video_analytics(
        self,
        video_ids: list[str],
        start_date: str,
        end_date: str,
        access_token: str,
        refresh_token: str | None = None,
    ) -> list[dict]:
        analytics = self.auth.get_analytics_service(access_token, refresh_token)
        result = defaultdict(lambda: {"views": 0, "likes": 0, "comments": 0})

        try:
            response = analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date,
                endDate=end_date,
                metrics="views,likes,comments",
                dimensions="day",
                filters=f"video=={','.join(video_ids)}"
            ).execute()

            rows = response.get("rows", [])
            for row in rows:
                date = row[0]
                result[date]["views"] += int(row[1])
                result[date]["likes"] += int(row[2])
                result[date]["comments"] += int(row[3])

        except HttpError as e:
            print(f"[WARN] Analytics error: {e}")

        # Trả về dạng list[dict] như FE mong muốn
        return [
            {
                "date": date,
                "views": stats["views"],
                "likes": stats["likes"],
                "comments": stats["comments"]
            }
            for date, stats in sorted(result.items(), reverse=True)
        ]

"""
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
            return [self._normalize_youtube_video_data(item) for item in response.get("items", [])]
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
            return [self._normalize_youtube_video_data(item) for item in response.get("items", [])]
        except Exception as e:
            raise RuntimeError(f"Không thể tìm kiếm video từ YouTube: {e}") from e



    def get_video_stats_list(self, video_ids: list[str], start_date: str, end_date: str, access_token: str, refresh_token: str|None = None) -> list[list]:
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

"""