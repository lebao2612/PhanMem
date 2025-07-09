from app.models import User
from app.dtos import VideoDTO
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

    def fetch_trending_videos(self, region: str = "VN", limit: int = 10) -> list[VideoDTO]:
        try:
            videos = self.youtube_client.trending_videos(region=region, limit=limit)
            return [VideoDTO.from_model(video) for video in videos]
        except Exception as e:
            raise HandledException(message=f"Failed to fetch trending videos: {str(e)}", code=500)

    def fetch_search_results(self, keyword: str, region: str = "VN", limit: int = 10) -> list[VideoDTO]:
        try:
            videos = self.youtube_client.fetch_search_results(keyword=keyword, region=region, limit=limit)
            return [VideoDTO.from_model(video) for video in videos]
        except Exception as e:
            raise HandledException(message=f"Search failed: {str(e)}", code=500)

    async def upload_video(self, creator: User, video_id: str, **kwargs) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException(message="Video not found", code=404)
        if video.youtube:
            raise HandledException(message="Video has already been uploaded", code=409)
        if video.status != "done" or not video.video_file:
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
                video_url=video.get_video_url(),
                **kwargs
            )

            video = self.video_repo.update_youtube(video=video, **video_detail)
            return VideoDTO.from_model(video=video)
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(code=500, message=f"Upload failed: {e}") from e

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
