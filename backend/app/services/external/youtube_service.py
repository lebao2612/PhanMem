from app.models import User
from app.dtos import VideoDTO
from app.exceptions import HandledException
from app.repositories import VideoRepository, UserRepository
from app.integrations import YouTubeClient, GoogleOAuthClient
import traceback


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


    def get_video_stats_list(self, creator: User, video_ids: list[str], start_date: str, end_date: str) -> list[list]:
        try:
            # Truy vấn MongoDB để lấy title theo video_id
            videos = self.video_repo.query(youtube_id__in=video_ids)

            # In log kiểm tra từng video
            for v in videos:
                print(f"📹 video_id: {v.youtube.id if v.youtube else 'None'}")

            video_titles = {
                # v.youtube.id: v.youtube.title if v.youtube and v.youtube.title else "" for v in videos
                v.youtube.id: v.youtube.title if v.youtube.title else ""
                for v in videos
                if v.youtube and v.youtube.id
            }

            # Gọi API YouTube Analytics
            raw_stats = self.youtube_client.get_video_stats_list(
                video_ids=video_ids,
                start_date=start_date,
                end_date=end_date,
                access_token=creator.google.access_token,
                refresh_token=creator.google.refresh_token
            )

            result = []
            for stat in raw_stats:
                video_id = stat[0]
                result.append([
                    video_id,
                    video_titles.get(video_id, ""),  # title
                    stat[1],  # views
                    stat[2],  # likes
                    stat[3],  # comments
                    stat[4],  # shares
                ])

            return {
                "success": True,
                "data": result
            }

        except Exception as e:
            print("❌ Traceback:")
            traceback.print_exc()  # In đầy đủ lỗi gốc
            raise HandledException(code=500, message=f"Failed to get total stats: {e}") from e

