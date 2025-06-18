from mongoengine import EmbeddedDocument, StringField

class MediaInfo(EmbeddedDocument):
    public_id = StringField()
    url = StringField()