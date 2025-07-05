from app.repositories import VideoRepository
from app.exceptions import HandledException
from app.dtos import VideoDTO

class VideoService:
    @staticmethod
    def get_video_by_id(video_id: str) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        return VideoDTO.from_model(video)

    @staticmethod
    def query_videos(filters: dict) -> list[VideoDTO]:
        videos = VideoRepository.query(filters)
        return [VideoDTO.from_model(v) for v in videos]


    @staticmethod
    def delete_video(video_id: str) -> bool:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        VideoRepository.delete_video(video)
        return True
