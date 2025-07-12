from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError
from app.utils import time_util
from app.models import (
    User,
    Video, VideoScene,
    Media, VideoMedia, ImageMedia, VoiceMedia,
    YoutubeVideoMetadata
)
from app.database import MongoDBConnection


class VideoRepository:
    def __init__(self, conn: MongoDBConnection):
        self.conn = conn

    def create_video(
        self,
        creator: User,
        topic: str,
        scenes: list[dict],
        src: dict,
        title: str="Untitled",
        status: str="draft"
    ) -> Video:
        try:
            filtered_src = {k: v for k, v in src.items() if hasattr(VideoMedia, k)}
            filtered_scenes = [
                {k: v for k, v in scene.items() if hasattr(VideoScene, k)}
                for scene in scenes
            ]

            video = Video(
                title=title,
                topic=topic,
                creator=creator,
                sources=VideoMedia(**filtered_src),
                scenes=[VideoScene(**scene) for scene in filtered_scenes],
                status=status
            )
            video.save(using=self.conn.alias)
            return video
        except ValidationError as e:
            raise ValueError(f"Dữ liệu video không hợp lệ: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Không thể tạo video: {e}") from e

    def find_by_id(self, video_id: str) -> Video | None:
        try:
            return Video.objects.using(self.conn.alias).get(id=video_id)
        except (DoesNotExist, ValidationError):
            return None
        except Exception as e:
            raise RuntimeError("Lỗi khi tìm video theo ID.") from e

    def query(self, **filters) -> list[Video]:
        try:
            query = Video.objects.using(self.conn.alias)
            filter_kwargs = {}

            if creator_id := filters.get("creator_id"):
                filter_kwargs["creator"] = ObjectId(creator_id)
            if title := filters.get("title"):
                filter_kwargs["title__icontains"] = title
            if topic := filters.get("topic"):
                filter_kwargs["topic__icontains"] = topic

            if filter_kwargs:
                query = query.filter(**filter_kwargs)

            sort_by = filters.get("sort", "-created_at")
            query = query.order_by(sort_by)

            skip = int(filters.get("skip", 0))
            limit = int(filters.get("limit", 20))
            query = query.skip(skip).limit(limit)

            return list(query)
        except Exception as e:
            raise RuntimeError("Lỗi khi truy vấn danh sách video.") from e

    def update_status(self, video: Video, status: str) -> Video:
        return self.update_fields(video, status=status)

    def update_sources(self, video: Video, url: str, public_id: str, **kwargs) -> Video:
        sources=VideoMedia(url=url, public_id=public_id)
        for k, v in kwargs.items():
            if hasattr(sources, k):
                setattr(sources, k, v)
        
        return self.update_fields(video=video, sources=sources)

    def update_youtube(self, video: Video, **kwargs) -> Video:
        try:
            if video.youtube:
                for k, v in kwargs.items():
                    if hasattr(video.youtube, k):
                        setattr(video.youtube, k, v)
            else:
                if kwargs.get("id"):
                    video.youtube = YoutubeVideoMetadata(**kwargs)
                else:
                    raise ValueError("Thiếu ID video YouTube.")

            video.updated_at = time_util.datetime_now()
            video.save(using=self.conn.alias)
            return video
        except ValidationError as e:
            raise ValueError(f"Dữ liệu YouTube không hợp lệ: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi khi cập nhật thông tin YouTube: {e}") from e

    def update_fields(self, video: Video, **kwargs) -> Video:
        try:
            for k, v in kwargs.items():
                if hasattr(video, k):
                    setattr(video, k, v)

            video.updated_at = time_util.datetime_now()
            video.save(using=self.conn.alias)
            return video
        except ValidationError as e:
            raise ValueError("Dữ liệu cập nhật không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Không thể cập nhật video.") from e

    def delete_video(self, video: Video) -> None:
        try:
            video.delete(using=self.conn.alias)
        except Exception as e:
            raise RuntimeError("Không thể xóa video.") from e
