from pydantic import BaseModel, Field
from typing import Optional, List


class GenerateScriptRequest(BaseModel):
    topic: str = Field(..., description="Topic for which the script will be generated")


class GenerateVoiceRequest(BaseModel):
    title: Optional[str] = Field(None, description="Video title")
    topic: str = Field(..., description="Video topic")
    script: str = Field(..., description="Script content")
    tags: Optional[List[str]] = Field(default=[], description="List of tags for the video")


class GenerateVideoRequest(BaseModel):
    video_id: str = Field(..., description="ID of the video to be generated")
