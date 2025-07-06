from mongoengine.errors import DoesNotExist, ValidationError
from app.utils import TimeUtil
from app.models import (
    User,
    Video, MediaInfo, VideoScene,
    YoutubeVideoMetadata
)

class VideoRepository:
    @staticmethod
    def create_draft_video(creator: User, topic: str) -> Video:
        try:
            video = Video(creator=creator, topic=topic, status="draft")
            video.save()
            return video
        except ValidationError as e:
            raise ValueError("Dữ liệu video không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Không thể tạo video nháp.") from e

    @staticmethod
    def find_by_id(video_id: str) -> Video | None:
        try:
            return Video.objects.get(id=video_id)
        except (DoesNotExist, ValidationError):
            return None
        except Exception as e:
            raise RuntimeError("Lỗi khi tìm video theo ID.") from e

    @staticmethod
    def query(**filters) -> list[Video]:
        try:
            query = Video.objects
            filter_kwargs = {}

            if creator_id := filters.get("creator_id"):
                filter_kwargs["creator__id"] = creator_id
            if title := filters.get("title"):
                filter_kwargs["title__icontains"] = title
            if topic := filters.get("topic"):
                filter_kwargs["topic__icontains"] = topic

            if filter_kwargs:
                query = query.filter(**filter_kwargs)

            # Sorting
            sort_by = filters.get("sort", "-created_at")
            query = query.order_by(sort_by)

            # Pagination
            skip = int(filters.get("skip", 0))
            limit = int(filters.get("limit", 20))
            query = query.skip(skip).limit(limit)

            return list(query)

        except Exception as e:
            raise RuntimeError("Lỗi khi truy vấn danh sách video.") from e

    @staticmethod
    def update_status(video: Video, status: str) -> Video:
        return VideoRepository.update_fields(video, status=status)

    @staticmethod
    def update_youtube(video: Video, **kwargs) -> Video:
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
            video.save()
            return video
        except ValidationError as e:
            raise ValueError("Dữ liệu YouTube không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Lỗi khi cập nhật thông tin YouTube.") from e

    @staticmethod
    def update_script(video: Video, script: list[dict]) -> Video:
        try:
            scenes = [
                VideoScene(**{k: v for k, v in s.items() if hasattr(VideoScene, k)})
                for s in script
            ]
            return VideoRepository.update_fields(video, script=scenes)
        except ValidationError as e:
            raise ValueError("Kịch bản không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Không thể cập nhật kịch bản.") from e

    @staticmethod
    def update_voice(video: Video, url: str, **kwargs) -> Video:
        return VideoRepository.update_fields(video, voice_file=MediaInfo(url=url, **kwargs))

    @staticmethod
    def update_video(video: Video, url: str, **kwargs) -> Video:
        return VideoRepository.update_fields(video, video_file=MediaInfo(url=url, **kwargs))

    @staticmethod
    def update_thumbnail(video: Video, url: str, **kwargs) -> Video:
        return VideoRepository.update_fields(video, thumbnail_file=MediaInfo(url=url, **kwargs))

    @staticmethod
    def update_fields(video: Video, **kwargs) -> Video:
        try:
            for k, v in kwargs.items():
                if hasattr(video, k):
                    setattr(video, k, v)

            video.updated_at = TimeUtil.now()
            video.save()
            return video
        except ValidationError as e:
            raise ValueError("Dữ liệu cập nhật không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Không thể cập nhật video.") from e

    @staticmethod
    def delete_video(video: Video) -> None:
        try:
            video.delete()
        except Exception as e:
            raise RuntimeError("Không thể xóa video.") from e
