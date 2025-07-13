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


###################
class TrimVideo(BaseSchema):
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")

class ThemeVideo(BaseSchema):
    class Music(BaseSchema):
        url: str = Field(..., description="URL of the background music")
        volume: float | None = Field(None, description="Volume level (0.0 to 1.0)")

    music: Music | None = Field(None, description="Music theme applied to the video")

class OverlayVideo(BaseSchema):
    class Sticker(BaseSchema):
        url: str = Field(..., description="URL of the sticker image")
        start: float = Field(..., description="Start time in seconds to show the sticker")
        end: float = Field(..., description="End time in seconds to hide the sticker")
        position: tuple[float, float] = Field(..., description="(x, y) position of the sticker")
        scale: float = Field(..., description="Scale factor for the sticker size")

    class Text(BaseSchema):
        text: str = Field(..., description="Text content to overlay")
        start: float = Field(..., description="Start time in seconds to show the text")
        end: float = Field(..., description="End time in seconds to hide the text")
        position: tuple[float, float] = Field(..., description="(x, y) position of the text")
        color: str = Field(..., description="Color of the text in hex format (e.g., '#FFFFFF')")

    stickers: list[Sticker] = Field(default_factory=list, description="List of stickers to overlay on the video")
    texts: list[Text] = Field(default_factory=list, description="List of text elements to overlay on the video")

class TimeLine(BaseSchema):
    pass  # Add fields if needed in the future

class EditVideoRequest(BaseSchema):
    trim: TrimVideo | None = Field(None, description="Trimming settings for the video")
    theme: ThemeVideo | None = Field(None, description="Theme or background music settings for the video")
    overlay: OverlayVideo | None = Field(None, description="Stickers and text overlays for the video")
