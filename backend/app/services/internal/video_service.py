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
    
    def get_youtube_ids_by_creator(self, creator_id: str) -> list[str]:
        videos = self.video_repo.query(
            creator_id=creator_id,
            youtube_uploaded_only=True,
            limit=1000
        )
        youtube_ids = []
        for video in videos:
            if video.youtube and video.youtube.id:
                youtube_ids.append(video.youtube.id)
            else:
                print(f"⚠️ Video thiếu metadata Youtube hoặc thiếu ID: {video}")
        return youtube_ids
