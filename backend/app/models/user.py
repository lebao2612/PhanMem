from mongoengine import Document, StringField, ListField, DateTimeField, DictField
from datetime import datetime, timezone
from .media_info import MediaInfo

class User(Document):
    # Google OAuth fields
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    googleId = StringField(unique=True, sparse=True)
    googleRefreshToken = StringField(required=True)
    picture = StringField(default=None)
    
    # Local authentication fields
    roles = ListField(StringField(), default=["USER"], choices=["USER", "ADMIN"])
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    lastLogin = DateTimeField()

    # 
    additionalPreferences = DictField(default={"theme": "dark", "language": "vi"})
    
    meta = {"collection": "users"}
