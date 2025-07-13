from mongoengine import (
    EmbeddedDocument, DateTimeField,
    StringField, IntField, ListField,
)
from app.utils import time_util

class Metadata(EmbeddedDocument):
    meta = {"allow_inheritance": True}
    id = StringField(required=True)

    # snippet
    title = StringField()
    description = StringField()
    tags = ListField(StringField(), default=[])

    # statitics
    views = IntField(default=0)
    likes = IntField(default=0)
    comments = IntField(default=0)
    shares = IntField(default=0)
    uploaded_at = DateTimeField(default=time_util.datetime_now)


class YoutubeVideoMetadata(Metadata):
    # analys
    analytic_date = DateTimeField()

    def get_video_url(self) -> str | None:
        if self.id:
            return f"https://www.youtube.com/watch?v={self.id}"
