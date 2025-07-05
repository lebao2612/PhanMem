from mongoengine.errors import DoesNotExist, ValidationError
from app.utils import TimeUtil
from app.exceptions import HandledException
from app.models import (
    User,
    Video, MediaInfo, VideoScene,
    YoutubeVideoMetadata
)


class VideoRepository:
    @staticmethod
    def create_draft_video(creator: User, topic: str) -> Video:
        try:
            video = Video(
                creator=creator,
                topic=topic,
                status="draft",
            )
            video.save()
            return video
        except Exception as e:
            raise HandledException(f"Failed to create video: {e}", 400)

    @staticmethod
    def find_by_id(video_id: str) -> Video | None:
        try:
            return Video.objects.get(id=video_id)
        except (DoesNotExist, ValidationError):
            return None
        except Exception as e:
            raise HandledException(f"Error finding video: {e}", 500)

    @staticmethod
    def query(creator_id: str=None, **kwargs) -> list[Video]:
        try:
            query = Video.objects

            # Filter by creator
            if creator_id:
                query = query.filter(creator=creator_id)

            # Filter by each field
            title = kwargs.get("title")
            if title:
                query = query.filter(title__icontains=title)

            topic = kwargs.get("topic")
            if topic:
                query = query.filter(topic__icontains=topic)

            # Sorting
            sort_by = kwargs.get("sort", "-created_at")
            query = query.order_by(sort_by)

            # Pagination
            skip = int(kwargs.get("skip", 0))
            limit = int(kwargs.get("limit", 20))
            query = query.skip(skip).limit(limit)

            return list(query)
        
        except Exception as e:
            raise HandledException(f"Error querying videos: {e}", 500)

    @staticmethod
    def update_status(video: Video, status: str) -> Video:
        return VideoRepository.update_fields(video, status=status)

    @staticmethod
    def update_youtube(video: Video, **kwargs) -> Video:
        try:
            if video.youtube:
                id = kwargs.pop("id", None)
                if id and video.youtube.id != id:
                    raise ValidationError("Video id does not match")
                
                for k, v in kwargs.items():
                    if hasattr(video.youtube, v):
                        setattr(video.youtube, k, v)
            else:
                if kwargs.get("id"):
                    video.youtube = YoutubeVideoMetadata(**kwargs)
                else:
                    raise DoesNotExist("Video id does not exist")
            
            # video.youtube.last_synced_at = TimeUtil.now()
            video.updated_at = TimeUtil.now()
            video.save()
            return video
        except Exception as e:
            raise HandledException(f"Failed to update with YouTube: {e}", 400)

    @staticmethod
    def update_script(video: Video, script: list[dict]) -> Video:
        return VideoRepository.update_fields(video, script=[VideoScene(**s) for s in script])

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
        except Exception as e:
            raise HandledException(f"Failed to update video: {e}", 400)

    @staticmethod
    def delete_video(video: Video) -> None:
        try:
            video.delete()
        except Exception as e:
            raise HandledException(f"Failed to delete video: {e}", 400)
