from mongoengine import (
    EmbeddedDocument, EmbeddedDocumentField,
    IntField, StringField, DateTimeField, ListField
)
from app.utils import TimeUtil


class YoutubeVideoSnippet(EmbeddedDocument):
    title = StringField()
    description = StringField()
    tags = ListField(StringField())
    category_id = StringField()
    channel_title = StringField()
    published_at = DateTimeField()

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "tags": self.tags or [],
            "category_id": self.category_id,
            "channel_title": self.channel_title,
            "published_at": self.published_at.isoformat() if self.published_at else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            tags=data.get("tags", []),
            category_id=data.get("category_id"),
            channel_title=data.get("channel_title"),
            published_at=TimeUtil.from_iso(data.get("published_at"))
        )


class YoutubeVideoStatus(EmbeddedDocument):
    privacy_status = StringField(choices=["public", "private", "unlisted"])
    upload_status = StringField()  # e.g. "processed", "uploaded", "deleted"

    def to_dict(self):
        return {
            "privacy_status": self.privacy_status,
            "upload_status": self.upload_status
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            privacy_status=data.get("privacy_status"),
            upload_status=data.get("upload_status")
        )


class YoutubeVideoStatistics(EmbeddedDocument):
    view_count = IntField(default=0)
    like_count = IntField(default=0)
    comment_count = IntField(default=0)

    def to_dict(self):
        return {
            "view_count": self.view_count,
            "like_count": self.like_count,
            "comment_count": self.comment_count
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            view_count=int(data.get("view_count", 0)),
            like_count=int(data.get("like_count", 0)),
            comment_count=int(data.get("comment_count", 0))
        )


# Nếu bạn muốn dùng sau này cho contentDetails như duration, caption...
class YoutubeVideoContentDetails(EmbeddedDocument):
    duration = StringField()  # ISO 8601 duration string: "PT1M52S", hoặc convert thành giây/int nếu muốn

    def to_dict(self):
        return {
            "duration": self.duration
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            duration=data.get("duration")
        )


class YoutubeVideoMetadata(EmbeddedDocument):
    video_id = StringField()
    snippet = EmbeddedDocumentField(YoutubeVideoSnippet)
    status = EmbeddedDocumentField(YoutubeVideoStatus)
    statistics = EmbeddedDocumentField(YoutubeVideoStatistics)
    # content_details = EmbeddedDocumentField(YoutubeVideoContentDetails)  # optional
    last_synced_at = DateTimeField()

    def get_video_url(self) -> str | None:
        return f"https://www.youtube.com/watch?v={self.video_id}" if self.video_id else None

    def to_dict(self):
        return {
            "id": self.video_id,
            "snippet": self.snippet.to_dict() if self.snippet else None,
            "status": self.status.to_dict() if self.status else None,
            "statistics": self.statistics.to_dict() if self.statistics else None,
            # "last_synced_at": self.last_synced_at.isoformat() if self.last_synced_at else None,
            # "content_details": self.content_details.to_dict() if self.content_details else None
        }

    @classmethod
    def from_dict(cls, item: dict):
        return cls(
            video_id=item.get("id"),
            snippet=YoutubeVideoSnippet.from_dict(item.get("snippet", {})),
            status=YoutubeVideoStatus.from_dict(item.get("status", {})),
            statistics=YoutubeVideoStatistics.from_dict(item.get("statistics", {})),
            # content_details=YoutubeVideoContentDetails.from_dict(item.get("content_details", {}))
            last_synced_at=TimeUtil.now(),
        )
