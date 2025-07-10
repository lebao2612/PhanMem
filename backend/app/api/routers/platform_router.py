from fastapi import APIRouter, Depends, Query
from app.schemas.requests import YouTubeUploadRequest
from app.schemas.responses import SuccessResponse
from app.api.middlewares import token_required
from app.dependencies import youtube_service
from app.models import User
from app.dtos import VideoDTO

router = APIRouter(prefix="/api/videos", tags=["youtube"])


@router.post("/youtube/upload/{video_id}", response_model=SuccessResponse[VideoDTO])
async def upload_youtube_video(
    video_id: str,
    data: YouTubeUploadRequest,
    current_user: User = Depends(token_required)):
    video = await youtube_service.upload_video(
        creator=current_user,
        video_id=video_id,
        **data.model_dump(exclude_none=True, by_alias=True)
    )
    return SuccessResponse(data=video)

@router.get("/youtube/refresh/{video_id}", response_model=SuccessResponse[VideoDTO])
def refresh_youtube_video(
    video_id: str,
    current_user: User = Depends(token_required)
):
    video = youtube_service.refresh_video(current_user, video_id)
    return SuccessResponse(data=video)

# @router.get("/youtube/refresh", response_model=SuccessResponse[VideoDTO])