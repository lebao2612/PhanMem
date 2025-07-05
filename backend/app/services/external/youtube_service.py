from app.models import User
from app.dtos import VideoDTO
from app.repositories import VideoRepository, UserRepository
from app.exceptions import HandledException
from app.integrations import YouTubeClient, GoogleOAuthClient
from app.utils import TimeUtil
from config import constants

class YoutubeService:
    @staticmethod
    def fetch_trending_videos(region: str = "VN", limit: int = 10) -> list:
        try:
            videos = YouTubeClient.trending_videos(region=region, limit=limit)
            
            return [VideoDTO.from_model(video) for video in videos]
        except Exception as e:
            raise HandledException(message=f"Failed to fetch trending videos: {str(e)}", code=500)

    @staticmethod
    def fetch_search_results(keyword: str, region: str = "VN", limit: int = 10) -> list:
        try:
            videos = YouTubeClient.fetch_search_results(keyword=keyword, region=region, limit=limit)

            return [VideoDTO.from_model(video) for video in videos]
        except Exception as e:
            raise HandledException(message=f"Search failed: {str(e)}", code=500)
    
    @staticmethod
    async def upload_video(creator: User, video_id: str, **kwargs) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException(message="Video not found", code=404)
        if video.youtube:
            raise HandledException(message="Video has already been uploaded", code=409)
        if video.status != "done" or not video.video_file:
            raise HandledException(message="Video has not been fully created yet", code=400)
        if not creator.google or not creator.google.refresh_token:
            raise HandledException(message="User has not logged in with Google", code=400)

        if creator.google.is_token_expired():
            tokens = GoogleOAuthClient.get_new_access_token(creator.google.refresh_token)
            creator = UserRepository.update_google(user=creator, **tokens)
        
        try:
            video_detail = await YouTubeClient.upload_video_url(
                refresh_token=creator.google.refresh_token,
                access_token=creator.google.access_token,
                video_url=video.get_video_url(),
                meta_kwargs=kwargs
            )
            
            video = VideoRepository.update_youtube(video=video, **video_detail)
            return VideoDTO.from_model(video=video)
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(code=500, message=f"Upload failed: {str(e)}")

    @staticmethod
    def refresh_video(creator: User, video_id: str) -> dict:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException(code=404, message="Video not found")
        if not creator.google or not creator.google.refresh_token:
            raise HandledException(message="User has not logged in with Google", code=400)
        if not video.youtube:
            raise HandledException(message="Video has not been uploaded", code=400)
        
        if creator.google.is_token_expired():
            tokens = GoogleOAuthClient.get_new_access_token(creator.google.refresh_token)
            creator = UserRepository.update_google(user=creator, **tokens)

        try:
            video_detail = YouTubeClient.get_video_details(
                video_id=str(video.id),
                access_token=creator.google.access_token,
                refresh_token=creator.google.refresh_token
            )

            video = VideoRepository.update_youtube(video, **video_detail)

            return VideoDTO.from_model(video=video)
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(code=500, message=f": {str(e)}")
