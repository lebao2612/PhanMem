from fastapi import APIRouter, Depends, Query, Path
from app.schemas.requests import YouTubeUploadRequest
from app.schemas.responses import SuccessResponse
from app.api.middlewares import token_required
from app.dependencies import youtube_service, video_service
from app.models import User
from app.dtos import VideoDTO

router = APIRouter(prefix="/api/videos", tags=["youtube"])


@router.post("/youtube/upload/{video_id}", response_model=SuccessResponse[VideoDTO])
async def upload_youtube_video(
    data: YouTubeUploadRequest,  # Request body with YouTube metadata
    video_id: str = Path(..., description="ID of the video to upload to YouTube"),
    current_user: User = Depends(token_required)  # Authenticated user
):
    video = await youtube_service.upload_video(
        creator=current_user,
        video_id=video_id,
        **data.model_dump(exclude_none=True, by_alias=True)
    )
    return SuccessResponse(data=video)


@router.get("/youtube/statistics", response_model=list[dict])
async def get_youtube_statistics(
    current_user: User = Depends(token_required),  # Authenticated user
):
    return await youtube_service.get_statistics(
        creator=current_user
    )

@router.get("/youtube/analytics", response_model=list[dict])
async def get_youtube_analytics(
    current_user: User = Depends(token_required),  # Authenticated user
    start_date: str = Query(None, alias="from", description="Start date (ISO format) for statistics range, eg: 2025-05-01T00:00:00"),
    end_date: str = Query(None, alias="to", description="End date (ISO format) for statistics range, eg: 2025-10-02")
):
    return await youtube_service.get_analytics(
        creator=current_user,
        start_date=start_date,
        end_date=end_date
    )

"""
@router.get("/youtube/refresh/{video_id}", response_model=SuccessResponse[VideoDTO])
def refresh_youtube_video(
    video_id: str = Path(..., description="ID of the YouTube video to refresh status"),
    current_user: User = Depends(token_required)  # Authenticated user
):
    video = youtube_service.refresh_video(current_user, video_id)
    return SuccessResponse(data=video)
"""