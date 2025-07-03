from mongoengine import (
    Document, StringField, ListField, DateTimeField, DictField,
    EmbeddedDocumentField
)
from .youtube_channel_info import YoutubeChannelInfo
from .google_oauth_info import GoogleOAuthInfo
from app.utils import TimeUtil

class User(Document):
    # Google OAuth fields
    name = StringField(required=True)
    email = StringField(required=True)
    
    google = EmbeddedDocumentField(GoogleOAuthInfo)
    youtube = EmbeddedDocumentField(YoutubeChannelInfo)

    picture = StringField()
    roles = ListField(StringField(), default=["USER"], choices=["USER", "ADMIN"])
    created_at = DateTimeField(default=TimeUtil.now)
    updated_at = DateTimeField(default=TimeUtil.now)
    # last_login = DateTimeField()

    additional_preferences = DictField(default={"theme": "dark", "language": "vi"})
    
    meta = {"collection": "users"}

    def has_role(self, required_roles: list[str]) -> bool:
        return any(role in self.roles for role in required_roles)
    def get_language(self) -> str | None:
        return self.additional_preferences.get("language")
    def get_theme(self) -> str | None:
        return self.additional_preferences.get("theme")
