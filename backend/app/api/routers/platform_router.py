from fastapi import APIRouter, Depends, Query
from app.schemas.requests import YouTubeUploadSchema
from app.schemas.responses import SuccessResponse
from app.api.middlewares import token_required
from app.services import YoutubeService
from app.models import User
from app.dtos import VideoDTO

router = APIRouter(prefix="/api/videos", tags=["youtube"])


@router.get("/youtube/trending", response_model=SuccessResponse[list[VideoDTO]])
def youtube_trending_videos(
    region = Query(default="VN",description=""),
    limit = Query(default=5, ge=1, le=20, description=""),
    current_user: User = Depends(token_required)
):
    videos = YoutubeService.fetch_trending_videos(region=region, limit=limit)
    return SuccessResponse(data=videos)

@router.get("/youtube/search", response_model=SuccessResponse[list[VideoDTO]])
def search_youtube_videos(
    keyword = Query(default=..., description=""),
    region = Query(default="VN",description=""),
    limit = Query(default=5, ge=1, le=20, description=""),
    current_user: User = Depends(token_required)
):
    videos = YoutubeService.fetch_search_results(keyword=keyword, region=region, limit=limit)
    return SuccessResponse(data=videos)

@router.post("/youtube/upload/{video_id}", response_model=SuccessResponse[VideoDTO])
async def upload_youtube_video(
    video_id: str,
    data: YouTubeUploadSchema,
    current_user: User = Depends(token_required)):
    video = await YoutubeService.upload_video(
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
    video = YoutubeService.refresh_video(current_user, video_id)
    return SuccessResponse(data=video)
