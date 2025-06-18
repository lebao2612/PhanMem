from app.models import Video
from mongoengine.errors import DoesNotExist, ValidationError
from typing import Optional, List
from datetime import datetime, timezone


class VideoRepository:
    @staticmethod
    def create_video(data: dict) -> Video:
        video = Video(**data)
        video.save()
        return video

    @staticmethod
    def find_by_id(video_id: str) -> Optional[Video]:
        try:
            return Video.objects.get(id=video_id)
        except (DoesNotExist, ValidationError):
            return None

    @staticmethod
    def find_by_creator(user_id: str, skip: int = 0, limit: int = 20) -> List[Video]:
        return list(Video.objects(creator=user_id).skip(skip).limit(limit))

    @staticmethod
    def list_all(skip: int = 0, limit: int = 20) -> List[Video]:
        return list(Video.objects.skip(skip).limit(limit))

    @staticmethod
    def search_by_topic_or_title(keyword: str, limit: int = 20) -> List[Video]:
        return list(Video.objects.filter(
            __raw__={
                "$or": [
                    {"title": {"$regex": keyword, "$options": "i"}},
                    {"topic": {"$regex": keyword, "$options": "i"}}
                ]
            }
        ).limit(limit))

    @staticmethod
    def update_fields(video: Video, update_data: dict, allowed_fields: List[str]) -> Video:
        for field in allowed_fields:
            if field in update_data:
                setattr(video, field, update_data[field])
        video.updated_at = datetime.now(timezone.utc)
        video.save()
        return video

    @staticmethod
    def update_status(video: Video, status: str) -> None:
        video.status = status
        video.updated_at = datetime.now(timezone.utc)
        video.save()

    @staticmethod
    def increment_views(video: Video) -> None:
        video.update(inc__views=1)

    @staticmethod
    def like_video(video: Video) -> None:
        video.update(inc__likes=1)

    @staticmethod
    def delete_video(video: Video) -> None:
        video.delete()
