from pydantic import Field, field_validator
from app.schemas.base_schema import BaseSchema

##
class GenerateScriptRequest(BaseSchema):
    topic: str = Field(..., description="Topic for which the script will be generated")
##
class RegenerateScriptRequest(BaseSchema):
    video_id: str = Field(..., description="ID of the video to regenerate the script for")

##
class SceneInput(BaseSchema):
    label: str = Field(..., min_length=1, description="Mô tả hình ảnh")
    subtitle: str = Field(..., min_length=1, description="Phụ đề sinh động")

    @field_validator("label", "subtitle", mode="before")
    @classmethod
    def validate_not_blank(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Phải là chuỗi không rỗng")
        return v.strip()    
class GenerateVoiceRequest(BaseSchema):
    video_id: str = Field(..., description="ID của video cần tạo voice")
    script: list[SceneInput] = Field(..., min_items=1, description="Danh sách cảnh (label + subtitle)")
    gender: str = Field(default="")

##
class GenerateVideoRequest(BaseSchema):
    video_id: str = Field(..., description="ID of the video to be generated")
