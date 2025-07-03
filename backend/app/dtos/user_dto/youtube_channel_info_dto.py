from pydantic import Field
from app.models import YoutubeChannelInfo
from app.dtos.base_dto import BaseDTO

class YoutubeChannelInfoDTO(BaseDTO):
    channel_id: str = Field(alias="channelId")
    title: str
    description: str

    @classmethod
    def from_model(cls, channel: YoutubeChannelInfo):
        return cls(
            channel_id=channel.channel_id,
            title=channel.snippet.title if channel.snippet else "Untitled",
            description=channel.snippet.description if channel.snippet else None
        )
