from mongoengine.errors import DoesNotExist, ValidationError
from app.utils import TimeUtil
from app.models import (
    User,
    Video, MediaInfo, VideoScene,
    YoutubeVideoMetadata
)
from app.database import MongoDBConnection

from bson import ObjectId


class VideoRepository:
    def __init__(self, conn: MongoDBConnection):
        self.conn = conn

    def create_draft_video(self, creator: User, topic: str) -> Video:
        try:
            video = Video(creator=creator, topic=topic, status="draft")
            video.save(using=self.conn.alias)
            return video
        except ValidationError as e:
            raise ValueError("Dữ liệu video không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Không thể tạo video nháp.") from e

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

    def update_youtube(self, video: Video, **kwargs) -> Video:
        try:
            if video.youtube:
                id = kwargs.pop("id", None)
                if id and video.youtube.id != id:
                    raise ValueError("Video ID không trùng khớp.")

                for k, v in kwargs.items():
                    if hasattr(video.youtube, k):
                        setattr(video.youtube, k, v)
            else:
                if kwargs.get("id"):
                    video.youtube = YoutubeVideoMetadata(**kwargs)
                else:
                    raise ValueError("Thiếu ID video YouTube.")

            video.updated_at = TimeUtil.now()
            video.save(using=self.conn.alias)
            return video
        except ValidationError as e:
            raise ValueError("Dữ liệu YouTube không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Lỗi khi cập nhật thông tin YouTube.") from e

    def update_script(self, video: Video, script: list[dict]) -> Video:
        try:
            scenes = [
                VideoScene(**{k: v for k, v in s.items() if hasattr(VideoScene, k)})
                for s in script
            ]
            return self.update_fields(video, script=scenes)
        except ValidationError as e:
            raise ValueError("Kịch bản không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Không thể cập nhật kịch bản.") from e

    def update_voice(self, video: Video, url: str, **kwargs) -> Video:
        return self.update_fields(video, voice_file=MediaInfo(url=url, **kwargs))

    def update_video(self, video: Video, url: str, **kwargs) -> Video:
        return self.update_fields(video, video_file=MediaInfo(url=url, **kwargs))

    def update_thumbnail(self, video: Video, url: str, **kwargs) -> Video:
        return self.update_fields(video, thumbnail_file=MediaInfo(url=url, **kwargs))

    def update_fields(self, video: Video, **kwargs) -> Video:
        try:
            for k, v in kwargs.items():
                if hasattr(video, k):
                    setattr(video, k, v)

            video.updated_at = TimeUtil.now()
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
