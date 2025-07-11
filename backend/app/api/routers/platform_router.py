from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Query
from app.schemas.requests import YouTubeUploadRequest
from app.schemas.responses import SuccessResponse
from app.api.middlewares import token_required
from app.dependencies import youtube_service, video_service
from app.models import User
from app.dtos import VideoDTO

router = APIRouter(prefix="/api/videos", tags=["youtube"])


@router.get("/youtube/trending", response_model=SuccessResponse[list[VideoDTO]])
def youtube_trending_videos(
    region = Query(default="VN",description=""),
    limit = Query(default=5, ge=1, le=20, description=""),
    current_user: User = Depends(token_required)
):
    videos = youtube_service.fetch_trending_videos(region=region, limit=limit)
    return SuccessResponse(data=videos)

@router.get("/youtube/search", response_model=SuccessResponse[list[VideoDTO]])
def search_youtube_videos(
    keyword = Query(default=..., description=""),
    region = Query(default="VN",description=""),
    limit = Query(default=5, ge=1, le=20, description=""),
    current_user: User = Depends(token_required)
):
    videos = youtube_service.fetch_search_results(keyword=keyword, region=region, limit=limit)
    return SuccessResponse(data=videos)

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

@router.get("/youtube/summary")
def get_video_stats_summary(
    current_user: User = Depends(token_required),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    creator_id = str(current_user.id)

    # Mặc định 7 ngày gần nhất
    today = datetime.today().date()
    end_date = end_date or today.isoformat()
    start_date = start_date or (today - timedelta(days=7)).isoformat()

    # B1: lấy video_ids
    video_ids = video_service.get_youtube_ids_by_creator(creator_id)

    if not video_ids:
        return {"message": "Không có video nào"}

    # B2: gọi API Analytics
    stats = youtube_service.get_total_stats(creator=current_user, video_ids=video_ids, start_date=start_date, end_date=end_date)

    return {
        **stats
    }
