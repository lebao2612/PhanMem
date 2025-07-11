from pydantic import Field
from app.dtos.base_dto import BaseDTO
from app.models import (
    Media,
)

class MediaDTO(BaseDTO):
    public_id: str = Field(..., alias='publicId')
    url: str = Field(...)

    @classmethod
    def from_model(cls, media: Media):
        return cls(
            public_id=media.public_id,
            url=media.url
        )