from app.models import User
from app.repositories import VideoRepository
from app.exceptions import HandledException
from app.integrations import YouTubeClient, GoogleOAuthClient

class YoutubeService:
    @staticmethod
    def fetch_treding_videos(
        region: str = "VN",
        limit: int = 10) -> list:
        try:
            return YouTubeClient.fetch_trending_videos(
                region=region,
                limit=limit,
            )
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Failed to fetch trending videos: {str(e)}")


    @staticmethod
    async def upload_video(
        creator: User,
        video_id: str,
        title: str,
        description: str,
        category: str = "22",
        privacy: str = "private",
        tags: list = ["AI"],
        ) -> dict:

        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException(status_code=404, detail="Video not found")
        if video.creator.id != creator.id:
            raise HandledException(status_code=403, detail="You do not have permission to upload this video")
        
        video_url = video.get_video_url()
        if not video_url:
            raise HandledException(status_code=400, detail="Video has not been fully created yet")
        
        refresh_token = creator.googleRefreshToken
        access_token = GoogleOAuthClient.get_new_access_token(refresh_token)

        try:
            response = await YouTubeClient.upload_video_url(
                refresh_token=refresh_token,
                access_token=access_token,
                video_url=video_url,
                title=title,
                description=description,
                category=category,
                privacy=privacy,
                tags=tags
            )

            return {
                "message": "Upload thành công",
                "video_id": response["id"]
            }
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Upload failed: {str(e)}")

    @staticmethod
    def stats_video(creator: User, video_id: str) -> dict:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException(status_code=404, detail="Video not found")
        if video.creator.id != creator.id:
            raise HandledException(status_code=403, detail="You do not have permission to upload this video")
        
        try:
            refresh_token = creator.googleRefreshToken
            access_token = GoogleOAuthClient.get_new_access_token(refresh_token)
            return YouTubeClient.fetch_video_stats(
                video_id=video_id,
                refresh_token=refresh_token,
                access_token=access_token
            )
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Thống kê lỗi: {str(e)}")
        
    @staticmethod
    def get_youtube_channel_id(creator: User) -> str:
        try:
            refresh_token = creator.googleRefreshToken
            access_token = GoogleOAuthClient.get_new_access_token(refresh_token)
            
            return YouTubeClient.get_channel_id(
                refresh_token=refresh_token,
                access_token=access_token
            )
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Lấy ID kênh thất bại: {str(e)}")

