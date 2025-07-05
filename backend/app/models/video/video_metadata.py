from mongoengine import (
    EmbeddedDocument, DateTimeField,
    StringField, IntField, ListField,
)

class VideoMetadata(EmbeddedDocument):
    meta = {"allow_inheritance": True}
    id = StringField(required=True)

    # snippet
    title = StringField()
    description = StringField()
    tags = ListField(StringField(), default=[])

    # statitics
    view_count = IntField(default=0)
    like_count = IntField(default=0)
    comment_count = IntField(default=0)

class YoutubeVideoMetadata(VideoMetadata):
    # last_synced_at = DateTimeField(default=TimeUtil.now)

    def get_youtube_url(self) -> str | None:
        if self.id:
            return f"https://www.youtube.com/watch?v={self.id}"
