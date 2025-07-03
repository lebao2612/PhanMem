from fastapi import APIRouter, Depends, Query
from app.schemas.requests import YouTubeUploadSchema
from app.schemas.responses import SuccessResponse
from app.api.middlewares import token_required
from app.services import YoutubeService
from app.models import User

router = APIRouter(prefix="/api/videos", tags=["youtube"])


@router.get("/youtube/trending", response_model=SuccessResponse[list])
def youtube_trending_videos(
    region = Query(default="VN",description=""),
    limit = Query(default=5, ge=1, le=20, description=""),
    current_user: User = Depends(token_required)
):
    stats = YoutubeService.fetch_trending_videos(region=region, limit=limit)
    return SuccessResponse(data=stats)

@router.get("/youtube/search", response_model=SuccessResponse[list])
def search_youtube_videos(
    keyword = Query(default=..., description=""),
    region = Query(default="VN",description=""),
    limit = Query(default=5, ge=1, le=20, description=""),
    current_user: User = Depends(token_required)
):
    stats = YoutubeService.fetch_search_results(keyword=keyword, region=region, limit=limit)
    return SuccessResponse(data=stats)


@router.post("/youtube/upload/{video_id}", response_model=SuccessResponse[dict])
async def upload_youtube_video(
    video_id: str,
    data: YouTubeUploadSchema,
    current_user: User = Depends(token_required)):
    result = await YoutubeService.upload_video(
        current_user,
        video_id, data.title, data.description, data.category, data.privacy
    )
    return SuccessResponse(data=result)

@router.get("/youtube/stats/{video_id}", response_model=SuccessResponse[dict])
def get_youtube_video_statistics(
    video_id: str,
    current_user: User = Depends(token_required)
):
    stats = YoutubeService.get_video_statistics(current_user, video_id)
    return SuccessResponse(data=stats)
