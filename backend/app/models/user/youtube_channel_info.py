from mongoengine import (
    EmbeddedDocument, EmbeddedDocumentField,
    StringField, DictField, IntField, DateTimeField
)
from app.utils import TimeUtil

class YoutubeChannelSnippet(EmbeddedDocument):
    title = StringField()
    description = StringField()
    published_at = DateTimeField()
    thumbnails = DictField()

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "thumbnails": self.thumbnails or {}
        }
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            published_at=TimeUtil.from_iso(data.get("published_at")),
            thumbnails=data.get("thumbnails", {})
        )


class YoutubeChannelStatistics(EmbeddedDocument):
    view_count = IntField()
    subscriber_count = IntField()
    video_count = IntField()
    # hidden_subscriber_count = BooleanField()

    def to_dict(self):
        return {
            "view_count": self.view_count,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count
        }
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            view_count=int(data.get("view_count", 0)),
            subscriber_count=int(data.get("subscriber_count", 0)),
            video_count=int(data.get("video_count", 0)),
        )


class YoutubeChannelStatus(EmbeddedDocument):
    privacy_status = StringField(choices=["public", "private", "unlisted"])
    # is_linked = StringField()

    def to_dict(self):
        return {
            "privacy_status": self.privacy_status
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            privacy_status=data.get("privacy_status", "private")
        )


# Coi là 1 kênh duy nhất
class YoutubeChannelInfo(EmbeddedDocument):
    channel_id = StringField()
    snippet = EmbeddedDocumentField(YoutubeChannelSnippet)
    statistic = EmbeddedDocumentField(YoutubeChannelStatistics)
    status = EmbeddedDocumentField(YoutubeChannelStatus)
    
    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "snippet": self.snippet.to_dict() if self.snippet else None,
            "statistics": self.statistic.to_dict() if self.statistic else None,
            "status": self.status.to_dict() if self.status else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            channel_id=data.get("id"),
            snippet=YoutubeChannelSnippet.from_dict(data.get("snippet", {})),
            statistic=YoutubeChannelStatistics.from_dict(data.get("statistics", {})),
            status=YoutubeChannelStatus.from_dict(data.get("status", {})),
        )