from fastapi import APIRouter, Depends
from app.schemas.requests import YouTubeUploadSchema
from app.schemas.responses import SuccessResponse
from app.api.middlewares import token_required
from app.services import PlatformService
from app.models import User
router = APIRouter(prefix="/api/platforms", tags=["platforms"])

# 
@router.post("/youtube/upload/{video_id}", response_model=SuccessResponse[dict])
def upload_youtube(
    video_id: str,
    data: YouTubeUploadSchema,
    current_user: User = Depends(token_required)):
    result = PlatformService.upload_youtube(current_user, video_id, data.title, data.description, data.category, data.privacy)
    return SuccessResponse(data=result)

@router.get("/youtube/stats/{video_id}", response_model=SuccessResponse[dict])
def stats_youtube(
    video_id: str,
    current_user: User = Depends(token_required)
):
    stats = PlatformService.stats_youtube(current_user, video_id)
    return SuccessResponse(data=stats)


@router.get("/youtube/channel_id/{video_id}", response_model=SuccessResponse[str])
def get_youtube_channel_id(
    current_user: User = Depends(token_required)
):
    channel_id = PlatformService.get_youtube_channel_id(current_user)
    return SuccessResponse(data=channel_id)
