from typing import Optional, List
from datetime import datetime, timezone
from app.repository import VideoRepository
from app.models import Video, User, MediaInfo
from app.dtos import VideoDTO
from app.integrations import *
from app.exceptions import HandledException

class VideoService:
    @staticmethod
    def create_video(title: str, topic: str, script: str, creator: User, tags: Optional[List[str]] = None) -> VideoDTO:
        video = Video(
            title=title,
            topic=topic,
            script=script,
            creator=creator,
            tags=tags or [],
            status="draft",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        VideoRepository.save(video)
        return VideoDTO.from_model(video)

    @staticmethod
    def get_video_by_id(video_id: str) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        return VideoDTO.from_model(video)

    @staticmethod
    def query_videos(filters) -> List[VideoDTO]:
        videos = VideoRepository.query(filters)
        return [VideoDTO.from_model(v) for v in videos]

    @staticmethod
    def update_video(
        video_id: str,
        update_data: dict,
        allowed_fields: List[str] = [
            "title", "topic", "script", "subtitles", "tags", "status",
            "video", "audio", "thumbnail", "views", "likes"
        ]
    ) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        updated = VideoRepository.update_fields(video, update_data, allowed_fields)
        return VideoDTO.from_model(updated)

    @staticmethod
    def delete_video(video_id: str) -> bool:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        VideoRepository.delete_video(video)
        return True