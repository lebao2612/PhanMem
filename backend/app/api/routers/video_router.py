from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.models import User
from app.dtos import VideoDTO
from app.schemas.requests import UpdateVideoRequest
from app.schemas.responses import SuccessResponse
from app.services import VideoService
from app.api.middlewares import token_required

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("/", response_model=SuccessResponse[List[VideoDTO]])
def list_all_videos(
    creator_id: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
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
    videos = VideoService.query_videos(filters)
    return SuccessResponse(data=videos)


@router.get("/me", response_model=SuccessResponse[List[VideoDTO]])
def list_my_videos(
    title: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
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
    videos = VideoService.query_videos(filters)
    return SuccessResponse(data=videos)


@router.get("/{video_id}", response_model=SuccessResponse[VideoDTO])
def get_video(video_id: str, current_user: User = Depends(token_required)):
    video = VideoService.get_video_by_id(video_id)
    return SuccessResponse(data=video)


@router.patch("/{video_id}", response_model=SuccessResponse[VideoDTO])
def update_video(video_id: str, data: UpdateVideoRequest, current_user: User = Depends(token_required)):
    video = VideoService.update_fields(video_id, data.model_dump(exclude_unset=True))
    return SuccessResponse(data=video)


@router.delete("/{video_id}", response_model=SuccessResponse[dict])
def delete_video(video_id: str, current_user: User = Depends(token_required)):
    VideoService.delete_video(video_id)
    return SuccessResponse(data=None)