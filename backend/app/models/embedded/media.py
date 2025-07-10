from mongoengine import (
    EmbeddedDocument,
    StringField, IntField
)

class Media(EmbeddedDocument):
    url = StringField(required=True)
    public_id = StringField()
    size = IntField(min_value=0)
    format = StringField()
    
    meta = {"allow_inheritance": True}

##
class VideoMedia(Media):
    thumbnail = StringField()
    duration = IntField(min_value=0)
    # format = StringField(choices=["mp4", "webm", "mkv", "avi"])

class VoiceMedia(Media):
    duration = IntField(min_value=0)
    # format = StringField(choices=["mp3", "wav"])

class ImageMedia(Media):
    width = IntField(min_value=0)
    height = IntField(min_value=0)
    # format = StringField(choices=["jpg", "png"])
