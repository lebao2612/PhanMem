from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError, OperationError
from app.utils import TimeUtil
from app.exceptions import HandledException
from app.models import (
    User,
    Video, MediaInfo, VideoScene,
    YoutubeVideoMetadata
)


class VideoRepository:
    @staticmethod
    def create_draft_video(topic: str, script: list[dict], creator: User) -> Video:
        try:
            video = Video(
                topic=topic,
                creator=creator,
                status="draft",
                script=[VideoScene.from_dict(scene) for scene in script]
            )
            video.save()
            return video
        except (ValidationError, NotUniqueError, OperationError) as e:
            raise HandledException(f"Tạo video thất bại: {e}", 400)

    @staticmethod
    def find_by_id(video_id: str) -> Video | None:
        try:
            return Video.objects.get(id=video_id)
        except (DoesNotExist, ValidationError):
            return None
        except Exception as e:
            raise HandledException(f"Lỗi khi tìm video: {e}", 500)

    @staticmethod
    def query(filters: dict) -> list[Video]:
        try:
            query = Video.objects

            # Lọc theo creator
            if filters.get("creator_id"):
                query = query.filter(creator=filters["creator_id"])

            # Lọc riêng từng trường
            if filters.get("title"):
                query = query.filter(title__icontains=filters["title"])
            if filters.get("topic"):
                query = query.filter(topic__icontains=filters["topic"])

            # Sắp xếp
            sort_by = filters.get("sort", "-created_at")
            query = query.order_by(sort_by)

            # Pagination
            skip = int(filters.get("skip", 0))
            limit = int(filters.get("limit", 20))
            query = query.skip(skip).limit(limit)

            return list(query)
        
        except Exception as e:
            raise HandledException(f"Lỗi khi truy vấn video: {e}", 500)

    @staticmethod
    def update_script(video: Video, script: list[dict]) -> Video:
        try:
            video.script = [VideoScene.from_dict(item) for item in script]
            video.updated_at = TimeUtil.now()
            video.save()
            return video
        except Exception as e:
            raise HandledException(f"Cập nhật script thất bại: {e}", 400)

    @staticmethod
    def update_status(video: Video, status: str) -> Video:
        try:
            video.status = status
            video.updated_at = TimeUtil.now()
            video.save()
            return video
        except Exception as e:
            raise HandledException(f"Cập nhật trạng thái thất bại: {e}", 400)

    @staticmethod
    def update_youtube(video: Video, youtube: dict) -> Video:
        try:
            video.youtube = YoutubeVideoMetadata.from_dict(youtube)
            video.updated_at = TimeUtil.now()
            video.save()
            return video
        except (KeyError, ValidationError) as e:
            raise
        except Exception as e:
            raise HandledException(f"Cập nhật trạng thái thất bại: {e}", 400)

    @staticmethod
    def update_voice(video: Video, public_id: str, url: str, format: str, size: int=0) -> Video:
        return VideoRepository._update_media(video, 'voice_file', public_id, url, format, size)

    @staticmethod
    def update_video(video: Video, public_id: str, url: str, format: str, size: int=0) -> Video:
        return VideoRepository._update_media(video, 'video_file', public_id, url, format, size)

    @staticmethod
    def update_thumbnail(video: Video, public_id: str, url: str, format: str, size: int=0) -> Video:
        return VideoRepository._update_media(video, 'thumbnail_file', public_id, url, format, size)
    
    @staticmethod
    def _update_media(video: Video, public_id: str, url: str, format: str, size: int, media_type: str) -> Video:
        try:
            media = MediaInfo(
                public_id=public_id,
                url=url,
                format=format,
                size=size
            )
            setattr(video, media_type, media)
            video.updated_at = TimeUtil.now()
            video.save()
            return video
        except Exception as e:
            raise HandledException(f"Cập nhật {media_type} thất bại: {e}", 400)

    @staticmethod
    def update_fields(video: Video, update_data: dict, allowed_fields: list[str]) -> Video:
        try:
            for field in allowed_fields:
                if field in update_data:
                    setattr(video, field, update_data[field])
            video.updated_at = TimeUtil.now()
            video.save()
            return video
        except Exception as e:
            raise HandledException(f"Cập nhật video thất bại: {e}", 400)

    @staticmethod
    def delete_video(video: Video) -> None:
        try:
            video.delete()
        except Exception as e:
            raise HandledException(f"Xóa video thất bại: {e}", 400)
