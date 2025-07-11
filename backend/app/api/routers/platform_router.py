from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from app.schemas.requests import YouTubeUploadRequest
from app.schemas.responses import SuccessResponse
from app.api.middlewares import token_required
from app.dependencies import youtube_service, video_service
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

@router.get("/youtube/video_stats")
def get_video_stats_summary(
    current_user: User = Depends(token_required),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    try:
        creator_id = str(current_user.id)
        today = datetime.today().date()
        end_date = end_date or today.isoformat()
        start_date = start_date or (today - timedelta(days=7)).isoformat()

        video_ids = video_service.get_youtube_ids_by_creator(creator_id)

        if not video_ids:
            return {"message": "Không có video nào"}

        stats = youtube_service.get_video_stats_list(
            creator=current_user,
            video_ids=video_ids,
            start_date=start_date,
            end_date=end_date
        )

        print("Stats: ", stats)

        return stats

    except Exception as e:
        print(f"🔥 Exception in /youtube/video_stats: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi truy vấn danh sách video: {e}")


# @router.get("/youtube/refresh", response_model=SuccessResponse[VideoDTO])