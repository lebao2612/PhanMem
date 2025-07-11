from app.repositories import VideoRepository
from app.dtos import VideoDTO
from app.exceptions import HandledException


class VideoService:
    def __init__(self, video_repo: VideoRepository):
        self.video_repo = video_repo

    def get_video_by_id(self, video_id: str) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        return VideoDTO.from_model(video)

    def query_videos(self, **filters) -> list[VideoDTO]:
        videos = self.video_repo.query(**filters)
        return [VideoDTO.from_model(v) for v in videos]

    def delete_video(self, video_id: str) -> bool:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        self.video_repo.delete_video(video)
        return True