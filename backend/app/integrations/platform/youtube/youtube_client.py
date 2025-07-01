from googleapiclient.http import MediaFileUpload
from app.exceptions import HandledException
from app.utils import FileUtil
from .youtube_auth import YouTubeAuth

class YouTubeClient:
    @staticmethod
    def trending_videos(
        region: str = "VN",
        limit: int = 10,
        ) -> list:
        #
        youtube = YouTubeAuth.get_public_service()
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode=region,
            maxResults=limit
        )
        response = request.execute()

        videos = []
        for item in response["items"]:
            video_id = item["id"]
            video = {
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "channelTitle": item["snippet"].get("channelTitle", ""),
                "publishedAt": item["snippet"].get("publishedAt", ""),
                "thumbnail": item["snippet"].get("thumbnails", {}).get("medium", {}).get("url", ""),
            }
            videos.append(video)
        return videos
    
    @staticmethod
    def search_videos(
        keyword: str,
        region: str = "VN",
        limit: int = 10
    ) -> list:
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

        videos = []
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video = {
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "channelTitle": item["snippet"].get("channelTitle", ""),
                "publishedAt": item["snippet"].get("publishedAt", ""),
                "thumbnail": item["snippet"].get("thumbnails", {}).get("medium", {}).get("url", ""),
            }
            videos.append(video)
        return videos

    @staticmethod
    async def upload_video_url(
        refresh_token: str,
        access_token: str,
        video_url: str,
        title: str,
        description: str,
        category: str,
        privacy: str,
        tags: list
    ) -> dict:
        temp_path = "upload_video_temp.mp4"

        try:
            await FileUtil.download_to_file(video_url, temp_path)

            return YouTubeClient.upload_video_file(
                refresh_token=refresh_token,
                access_token=access_token,
                file_path=temp_path,
                title=title,
                description=description,
                category=category,
                privacy=privacy,
                tags=tags
            )

        finally:
            FileUtil.delete_file(temp_path)

    @staticmethod
    def upload_video_file(
        refresh_token: str,
        access_token: str,
        file_path: str,
        title: str,
        description: str,
        category: str,
        privacy: str,
        tags: list
    ) -> dict:
        youtube = YouTubeAuth.get_auth_service(
            refresh_token=refresh_token,
            access_token=access_token
        )

        metadata = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
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
        try:
            while response is None:
                status, response = request.next_chunk()
        except Exception as e:
            raise HandledException(f"Lỗi khi upload video: {e}", 500)

        media.stream().close()
        return response

    @staticmethod
    def fetch_video_stats(video_id: str, refresh_token: str, access_token: str) -> dict:
        youtube = YouTubeAuth.get_auth_service(
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
        youtube = YouTubeAuth.get_auth_service(
            refresh_token=refresh_token,
            access_token=access_token
        )
        response = youtube.channels().list(part="id", mine=True).execute()
        return response["items"][0]["id"]
