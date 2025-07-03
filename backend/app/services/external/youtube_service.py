from app.models import User
from app.dtos import VideoDTO
from app.utils import DictUtil
from app.repositories import VideoRepository, UserRepository
from app.exceptions import HandledException
from app.integrations import YouTubeClient, GoogleOAuthClient
from config import constants

class YoutubeService:
    @staticmethod
    def fetch_trending_videos(region: str = "VN", limit: int = 10) -> list:
        try:
            trending_videos = YouTubeClient.trending_videos(region=region, limit=limit)
                        
            return trending_videos
        except Exception as e:
            raise HandledException(status_code=500, message=f"Failed to fetch trending videos: {str(e)}")

    @staticmethod
    def fetch_search_results(keyword: str, region: str = "VN", limit: int = 10) -> list:
        try:
            return YouTubeClient.search_videos(keyword=keyword, region=region, limit=limit)
        except Exception as e:
            raise HandledException(status_code=500, message=f"Tìm kiếm thất bại: {str(e)}")
    
    @staticmethod
    async def upload_video(
        creator: User,
        video_id: str,
        title: str,
        description: str,
        category: str = "22",
        privacy: str = "private",
        tags: list = ["AI"],
        ) -> VideoDTO:

        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException(status_code=404, message="Video not found")
        if video.creator.id != creator.id:
            raise HandledException(status_code=403, message="You do not have permission to upload this video")
        if video.status != "done" or not video.video_file:
            raise HandledException(status_code=400, message="Video has not been fully created yet")
        if video.youtube:
            raise HandledException(status_code=409, message="Video đã upload")
        if not creator.google or not creator.google.has_scope(constants.YOUTUBE_SCOPES["YOUTUBE_UPLOAD"]):
            raise HandledException(status_code=400, message="Người dùng không có quyền upload youtube")

        if creator.google.is_token_expired():
            tokens = GoogleOAuthClient.get_new_access_token(creator.google.refresh_token)
            creator = UserRepository.update_google_tokens(
                user=creator,
                tokens=tokens
            )

        metadata = YoutubeService._build_youtube_metadata(title, description, category, tags, privacy)
        
        try:
            response = await YouTubeClient.upload_video_url(
                refresh_token=creator.google.refresh_token,
                access_token=creator.google.access_token,
                video_url=video.get_video_url(),
                metadata=metadata
            )
            
            youtube =DictUtil.normalize_keys(response)
            video = VideoRepository.update_youtube(video=video, youtube=youtube)
            return VideoDTO.from_model(video=video)
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(status_code=500, message=f"Upload failed: {str(e)}")

    @staticmethod
    def get_video_statistics(creator: User, video_id: str) -> dict:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException(status_code=404, message="Video not found")
        if video.creator.id != creator.id:
            raise HandledException(status_code=403, message="You do not have permission to upload this video")
        
        try:
            refresh_token = creator.google_refresh_token
            access_token = GoogleOAuthClient.get_new_access_token(refresh_token)
            return YouTubeClient.fetch_video_stats(
                video_id=video_id,
                refresh_token=refresh_token,
                access_token=access_token
            )
        except Exception as e:
            raise HandledException(status_code=500, message=f"Thống kê lỗi: {str(e)}")
        
    @staticmethod
    def get_youtube_channel_id(creator: User) -> str:
        try:
            refresh_token = creator.google_refresh_token
            access_token = GoogleOAuthClient.get_new_access_token(refresh_token)
            
            return YouTubeClient.get_channel_info(
                refresh_token=refresh_token,
                access_token=access_token
            )
        except Exception as e:
            raise HandledException(status_code=500, message=f"Lấy ID kênh thất bại: {str(e)}")

    @staticmethod
    def _build_youtube_metadata(title: str, description: str, category: str, tags: list, privacy: str) -> dict:
        return {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category,
                "tags": tags,
            },
            "status": {
                "privacyStatus": privacy
            }
        }