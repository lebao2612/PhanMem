from typing import Optional
from pydantic import BaseModel
from app.models import MediaInfo


class MediaInfoDTO(BaseModel):
    url: Optional[str]

    @classmethod
    def from_model(cls, media: MediaInfo):
        return cls(
            url=media.url if media else None
        )
