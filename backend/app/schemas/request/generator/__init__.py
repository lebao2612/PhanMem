from pydantic import BaseModel


class GenerateScriptRequest(BaseModel):
    topic: str


class GenerateVoiceRequest(BaseModel):
    video_id: str


class GenerateVideoRequest(BaseModel):
    video_id: str
