from app.models import User
from app.dtos import VideoDTO
from app.utils import time_util
from app.exceptions import HandledException
from app.repositories import VideoRepository, UserRepository
from app.integrations import YouTubeClient, GoogleOAuthClient

class YoutubeService:
    def __init__(
        self,
        video_repo: VideoRepository,
        user_repo: UserRepository,
        youtube_client: YouTubeClient,
        google_oauth_client: GoogleOAuthClient,
    ):
        self.video_repo = video_repo
        self.user_repo = user_repo
        self.youtube_client = youtube_client
        self.google_oauth_client = google_oauth_client

    async def upload_video(self, creator: User, video_id: str, **kwargs) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException(message="Video not found", code=404)
        if video.youtube:
            raise HandledException(message="Video has already been uploaded", code=409)
        if not video.sources:
            raise HandledException(message="Video has not been fully created yet", code=400)
        if not creator.google or not creator.google.refresh_token:
            raise HandledException(message="User has not logged in with Google", code=400)

        if creator.google.is_token_expired():
            tokens = self.google_oauth_client.get_new_access_token(creator.google.refresh_token)
            creator = self.user_repo.update_google(user=creator, **tokens)

        try:
            video_detail = await self.youtube_client.upload_video_url(
                refresh_token=creator.google.refresh_token,
                access_token=creator.google.access_token,
                video_url=video.sources.url,
                **kwargs
            )

            video = self.video_repo.update_youtube(video=video, **video_detail)
            return VideoDTO.from_model(video=video)
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(code=500, message=f"Upload failed: {e}") from e

    async def get_statistics(
        self,
        creator: User
    ) -> list[dict]:
        if not creator.google or not creator.google.refresh_token:
            raise HandledException(message="User has not logged in with Google", code=400)
        if creator.google.is_token_expired():
            tokens = self.google_oauth_client.get_new_access_token(creator.google.refresh_token)
            creator = self.user_repo.update_google(user=creator, **tokens)

        youtube_videos  = self.video_repo.list_uploaded_youtube(creator=creator)
        if not youtube_videos:
            return []
        
        return await self.youtube_client.get_video_statistics(
            video_ids=[v.id for v in youtube_videos],
            access_token=creator.google.access_token,
            refresh_token=creator.google.refresh_token,
        )

    async def get_analytics(
        self,
        creator: User,
        start_date: str= None,
        end_date: str=None,
    ) -> list[dict]:
        if not creator.google or not creator.google.refresh_token:
            raise HandledException(message="User has not logged in with Google", code=400)
        if creator.google.is_token_expired():
            tokens = self.google_oauth_client.get_new_access_token(creator.google.refresh_token)
            creator = self.user_repo.update_google(user=creator, **tokens)

        youtube_videos = self.video_repo.list_uploaded_youtube(creator=creator)
        if not youtube_videos:
            return []
        
        if not start_date:
            start_date = time_util.datetime_to_str(time_util.datetime_delta(days=-7))
        if not end_date:
            end_date = time_util.datetime_to_str(time_util.datetime_now())

        return await self.youtube_client.get_video_analytics(
            video_ids=[v.id for v in youtube_videos],
            start_date=start_date,
            end_date=end_date,
            access_token=creator.google.access_token,
            refresh_token=creator.google.refresh_token,
        )

"""
    def refresh_video(self, creator: User, video_id: str) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException(code=404, message="Video not found")
        if not creator.google or not creator.google.refresh_token:
            raise HandledException(message="User has not logged in with Google", code=400)
        if not video.youtube:
            raise HandledException(message="Video has not been uploaded", code=400)

        if creator.google.is_token_expired():
            tokens = self.google_oauth_client.get_new_access_token(creator.google.refresh_token)
            creator = self.user_repo.update_google(user=creator, **tokens)

        try:
            video_detail = self.youtube_client.get_video_details(
                video_id=str(video.id),
                access_token=creator.google.access_token,
                refresh_token=creator.google.refresh_token
            )

            video = self.video_repo.update_youtube(video, **video_detail)
            return VideoDTO.from_model(video=video)
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(code=500, message=f": {e}") from e
"""