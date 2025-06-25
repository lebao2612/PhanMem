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
    def query(filters: dict) -> List[Video]:
        query = Video.objects

        # Lọc theo creator
        if filters.get("creator_id"):
            query = query.filter(creator=filters["creator_id"])

        # Search theo keyword (áp dụng trên title, topic, tags)
        keyword = filters.get("keyword")
        if keyword:
            query = query.filter(__raw__={
                "$or": [
                    {"title": {"$regex": keyword, "$options": "i"}},
                    {"topic": {"$regex": keyword, "$options": "i"}},
                    {"tags": {"$regex": keyword, "$options": "i"}}
                ]
            })

        # Lọc riêng từng trường
        if filters.get("title"):
            query = query.filter(title__icontains=filters["title"])
        if filters.get("topic"):
            query = query.filter(topic__icontains=filters["topic"])
        if filters.get("tags"):
            tags = filters["tags"]
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(",")]
            query = query.filter(tags__in=tags)

        # Sắp xếp
        sort_by = filters.get("sort", "-created_at")
        query = query.order_by(sort_by)

        # Pagination
        skip = int(filters.get("skip", 0))
        limit = int(filters.get("limit", 20))
        query = query.skip(skip).limit(limit)

        return list(query)

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
    def delete_video(video: Video) -> None:
        video.delete()
