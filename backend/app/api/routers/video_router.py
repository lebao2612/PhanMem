from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.services import VideoService, VideoUpload, handle_upload, get_video_stats
from app.models import User
from app.dtos import VideoDTO
from app.api.middlewares import token_required
from app.schemas.request.video import *

router = APIRouter(prefix="/api/videos", tags=["videos"])

@router.get("/", response_model=List[VideoDTO])
def list_all_videos(
    creator_id: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    sort: str = Query("-created_at"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(token_required)
):
    filters = {
        "creator_id": creator_id,
        "title": title,
        "topic": topic,
        "tags": tags,
        "keyword": keyword,
        "sort": sort,
        "skip": skip,
        "limit": limit,
    }
    return VideoService.query_videos(filters)


@router.get("/me", response_model=List[VideoDTO])
def list_my_videos(
    title: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    sort: str = Query("-created_at"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(token_required)
):
    filters = {
        "creator_id": str(current_user.id),
        "title": title,
        "topic": topic,
        "tags": tags,
        "keyword": keyword,
        "sort": sort,
        "skip": skip,
        "limit": limit,
    }
    return VideoService.query_videos(filters)


@router.get("/{video_id}", response_model=VideoDTO)
def get_video(video_id: str, current_user: User = Depends(token_required)):
    return VideoService.get_video_by_id(video_id)


@router.post("/", response_model=VideoDTO)
def create_video(data: CreateVideoRequest, current_user: User = Depends(token_required)):
    return VideoService.create_video(
        data.title, data.topic, data.script, current_user, data.tags
    )


@router.patch("/{video_id}", response_model=VideoDTO)
def update_video(video_id: str, data: UpdateVideoRequest, current_user: User = Depends(token_required)):
    return VideoService.update_video(video_id, data.model_dump(exclude_unset=True))


@router.delete("/{video_id}")
def delete_video(video_id: str, current_user: User = Depends(token_required)):
    VideoService.delete_video(video_id)
    return {"message": "Xóa video thành công"}

@router.post("/upload")
def upload_video(data: VideoUpload):
    return handle_upload(data)

@router.get("/stats")
def video_stats(video_id: str):
    return get_video_stats(video_id)