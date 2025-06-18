from app.models import Video

class VideoDTO:
    def __init__(
        self, id, title, topic, script, subtitles, video, audio, thumbnail,
        creator_id, status, tags, views, likes, created_at, updated_at
    ):
        self.id = id
        self.title = title
        self.topic = topic
        self.script = script
        self.subtitles = subtitles
        self.video = video  # Chỉ chứa url
        self.audio = audio  # Chỉ chứa url
        self.thumbnail = thumbnail  # Chỉ chứa url
        self.creator_id = creator_id
        self.status = status
        self.tags = tags
        self.views = views
        self.likes = likes
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_model(cls, video: Video):
        return cls(
            id=str(video.id),
            title=video.title,
            topic=video.topic,
            script=video.script,
            subtitles=video.subtitles,
            video=video.video.url if video.video else None,  # Chỉ lấy url
            audio=video.audio.url if video.audio else None,  # Chỉ lấy url
            thumbnail=video.thumbnail.url if video.thumbnail else None,  # Chỉ lấy url
            creator_id=str(video.creator.id) if video.creator else None,
            status=video.status,
            tags=video.tags,
            views=video.views,
            likes=video.likes,
            created_at=video.created_at.isoformat() if video.created_at else None,
            updated_at=video.updated_at.isoformat() if video.updated_at else None,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "topic": self.topic,
            "script": self.script,
            "subtitles": self.subtitles,
            "video": self.video,  # Chỉ chứa url
            "audio": self.audio,  # Chỉ chứa url
            "thumbnail": self.thumbnail,  # Chỉ chứa url
            "creator_id": self.creator_id,
            "status": self.status,
            "tags": self.tags,
            "views": self.views,
            "likes": self.likes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }