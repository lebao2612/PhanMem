from app.models import Video

class VideoDTO:
    def __init__(self, id, title, video_url, thumbnail_url, tags, created_at):
        self.id = id
        self.title = title
        self.video_url = video_url
        self.thumbnail_url = thumbnail_url
        self.tags = tags
        self.created_at = created_at

    @classmethod
    def from_model(cls, video: Video):
        return cls(
            id=str(video.id),
            title=video.title,
            video_url=video.video_url,
            thumbnail_url=video.thumbnail_url,
            tags=video.tags,
            created_at=video.created_at.isoformat() if video.created_at else None
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "video_url": self.video_url,
            "thumbnail_url": self.thumbnail_url,
            "tags": self.tags,
            "created_at": self.created_at,
        }
