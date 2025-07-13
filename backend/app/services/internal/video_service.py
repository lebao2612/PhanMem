from app.models import User
from app.dtos import VideoDTO
from app.utils import file_util
from app.modules import mediax
from app.exceptions import HandledException
from app.repositories import VideoRepository
from app.integrations import CloudinaryClient

class VideoService:
    def __init__(self, video_repo: VideoRepository, cloudinary_client: CloudinaryClient):
        self.video_repo = video_repo
        self.cloudinary_client = cloudinary_client

    def get_video_by_id(self, video_id: str) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        return VideoDTO.from_model(video)
    
    def list_by_creator(self, creator: User) -> list[VideoDTO]:
        videos = self.video_repo.query(creator=creator, limit=0)

        if videos:
            return [VideoDTO.from_model(video) for video in videos]
        
        return []

    def query_videos(self, **filters) -> list[VideoDTO]:
        filters = {k: v for k, v in filters.items() if v is not None}

        videos = self.video_repo.query(**filters)
        return [VideoDTO.from_model(v) for v in videos]

    def delete_video(self, video_id: str) -> bool:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        self.video_repo.delete_video(video)
        return True

    async def edit_video(self, creator: User, video_id: str, **option):
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException(message="Video not found", code=404)
        if not video.sources:
            raise HandledException(message="Video has not been fully created yet", code=400)
        if not option:
            return VideoDTO.from_model(video=video)

        try:
            tmp_path = await mediax.edit.edit_video(video.sources.url, **option)

            upload_res = await self.cloudinary_client.upload_from_path(
                file_path=tmp_path,
                resource_type="video",
                filename=video.sources.public_id
            )

            video = self.video_repo.update_sources(
                video=video,
                **upload_res
            )

        except Exception as e:
            raise HandledException(message=f"Error edit video: {e}", code=400)
        finally:
            file_util.delete_file(tmp_path)
