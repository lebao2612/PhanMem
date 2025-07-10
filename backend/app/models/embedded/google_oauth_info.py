from mongoengine import (
    StringField, DateTimeField,
    EmbeddedDocument
)
from app.utils import time_util

class GoogleOAuthInfo(EmbeddedDocument):
    sub = StringField(required=True)
    
    token_type = StringField(default="Bearer")
    refresh_token = StringField(required=True)
    access_token = StringField()
    expires_at = DateTimeField()

    def is_token_expired(self) -> bool:
        if not self.expires_at or not self.access_token:
            return True
        return time_util.datetime_now().timestamp() >= self.expires_at.timestamp()
