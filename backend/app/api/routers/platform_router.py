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


@router.get("/youtube/refresh/{video_id}", response_model=SuccessResponse[VideoDTO])
def refresh_youtube_video(
    video_id: str = Path(..., description="ID of the YouTube video to refresh status"),
    current_user: User = Depends(token_required)  # Authenticated user
):
    video = youtube_service.refresh_video(current_user, video_id)
    return SuccessResponse(data=video)


@router.get("/youtube/video_stats")
def get_video_stats_summary(
    current_user: User = Depends(token_required),  # Authenticated user
    start_date: str = Query(None, description="Start date (ISO format) for statistics range"),
    end_date: str = Query(None, description="End date (ISO format) for statistics range")
):
    raise NotImplementedError("Not implement")
    # Implementation is currently disabled

    # creator_id = str(current_user.id)

    # # Mặc định 7 ngày gần nhất
    # today = datetime.today().date()
    # end_date = end_date or today.isoformat()
    # start_date = start_date or (today - timedelta(days=7)).isoformat()

    # # B1: lấy video_ids
    # video_ids = video_service.get_youtube_ids_by_creator(creator_id)

    # if not video_ids:
    #     return {"message": "Không có video nào"}

    # # B2: gọi API Analytics
    # stats = youtube_service.get_video_stats_list(creator=current_user, video_ids=video_ids, start_date=start_date, end_date=end_date)

    # return stats
