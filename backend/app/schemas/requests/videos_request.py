from pydantic import Field
from app.schemas.base_schema import BaseSchema


class UpdateVideoRequest(BaseSchema):
    title: str | None = Field(
        None,
        description="Video title"
    )
    thumbnail: str | None = Field(
        None,
        description="Thumbnail image URL"
    )

####
class Trim(BaseSchema):
    start: float
    end: float

class Theme(BaseSchema):
    class Music(BaseSchema):
        url: str
        volume: float | None
    music: Music | None

class Overlay(BaseSchema):
    class Sticker(BaseSchema):
        url: str
        start: float
        end: float
        position: tuple[float,float]
        scale: float
    class Text(BaseSchema):
        text: str
        start: float
        position: tuple[float,float]
        end: float
        color: str
    
    stickers: list[Sticker]
    texts: list[Text]

class TimeLine(BaseSchema):
    pass

class EditVideoRequest(BaseSchema):
    trim: Trim | None
    theme: Theme | None
    overlay: Overlay | None
