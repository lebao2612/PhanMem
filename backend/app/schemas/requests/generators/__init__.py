from pydantic import BaseModel, Field
from typing import Optional, List


class GenerateScriptRequest(BaseModel):
    topic: str = Field(..., description="Topic for which the script will be generated")


class RegenerateScriptRequest(BaseModel):
    video_id: str = Field(..., description="ID of the video to regenerate the script for")


class GenerateVoiceRequest(BaseModel):
    video_id: str = Field(..., description="ID of the video to be generated")
    script: str = Field(..., description="Script to generate voice from")


class GenerateVideoRequest(BaseModel):
    video_id: str = Field(..., description="ID of the video to be generated")
