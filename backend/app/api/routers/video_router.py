from fastapi import APIRouter, Depends, Query
from app.models import User
from app.dtos import VideoDTO
from app.schemas.requests import UpdateVideoRequest, EditVideoRequest
from app.schemas.responses import SuccessResponse
from app.dependencies import video_service
from app.api.middlewares import token_required

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("/", response_model=SuccessResponse[list[VideoDTO]])
def list_all_videos(
    creator_id: str = Query(None),
    title: str = Query(None),
    topic: str = Query(None),
    sort: str = Query("-created_at"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(token_required)
):
    filters = {
        "creator_id": creator_id,
        "title": title,
        "topic": topic,
        "sort": sort,
        "skip": skip,
        "limit": limit,
    }
    videos = video_service.query_videos(**filters)
    return SuccessResponse(data=videos)


@router.get("/me", response_model=SuccessResponse[list[VideoDTO]])
def list_my_videos(
    title: str = Query(None),
    topic: str = Query(None),
    sort: str = Query("-created_at"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(token_required)
):
    filters = {
        "creator_id": str(current_user.id),
        "title": title,
        "topic": topic,
        "sort": sort,
        "skip": skip,
        "limit": limit,
    }
    videos = video_service.query_videos(**filters)
    return SuccessResponse(data=videos)


@router.get("/{video_id}", response_model=SuccessResponse[VideoDTO])
def get_video(video_id: str, current_user: User = Depends(token_required)):
    video = video_service.get_video_by_id(video_id)
    return SuccessResponse(data=video)


@router.delete("/{video_id}", response_model=SuccessResponse[None])
def delete_video(video_id: str, current_user: User = Depends(token_required)):
    video_service.delete_video(video_id)
    return SuccessResponse(data=None)

@router.put("/{video_id}", response_model=SuccessResponse[VideoDTO])
async def edit_video(video_id: str, data: EditVideoRequest , current_user: User = Depends(token_required)):
    video = await video_service.edit_video(
        creator=current_user,
        video_id=video_id,
        **data.model_dump(exclude_none=True, by_alias=True)
    )
    return SuccessResponse(data=video)
