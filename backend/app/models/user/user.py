from mongoengine import (
    Document, StringField, ListField, DateTimeField,
    EmbeddedDocumentField
)
from app.utils import TimeUtil
from .google_oauth_info import GoogleOAuthInfo
from .user_settings import UserSettings

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    # password = StringField()

    picture = StringField()
    roles = ListField(StringField(), default=["USER"], choices=["USER", "ADMIN"])
    google: GoogleOAuthInfo = EmbeddedDocumentField(GoogleOAuthInfo)

    created_at = DateTimeField(default=TimeUtil.now)
    updated_at = DateTimeField(default=TimeUtil.now)

    settings: UserSettings = EmbeddedDocumentField(UserSettings, default=UserSettings)
    
    meta = {"collection": "users"}

    def has_role(self, required_roles: list[str]) -> bool:
        return any(role in self.roles for role in required_roles)
