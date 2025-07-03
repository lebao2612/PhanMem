from app.models import VideoScene
from app.dtos.base_dto import BaseDTO

class VideoSceneDTO(BaseDTO):
    label: str
    subtitle: str

    @classmethod
    def from_model(cls, scene: VideoScene):
        return cls(
            label=scene.label,
            subtitle=scene.subtitle,
        )