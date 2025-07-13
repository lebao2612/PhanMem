from fastapi import APIRouter, Depends, Query, Path
from app.models import User
from app.dtos import VideoDTO
from app.schemas.requests import UpdateVideoRequest, EditVideoRequest
from app.schemas.responses import SuccessResponse
from app.dependencies import video_service
from app.api.middlewares import token_required

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("/me", response_model=SuccessResponse[list[VideoDTO]])
def list_my_videos(
    title: str = Query(None, description="Filter by video title"),
    topic: str = Query(None, description="Filter by video topic"),
    sort: str = Query("-created_at", description="Sort order, e.g. -created_at or title"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of videos to return"),
    current_user: User = Depends(token_required)  # Authenticated user
):

    videos = video_service.query_videos(
        creator=current_user,
        title=title,
        topic=topic,
        sort=sort,
        skip=skip,
        limit=limit
    )
    return SuccessResponse(data=videos)


@router.get("/{video_id}", response_model=SuccessResponse[VideoDTO])
def get_video(
    video_id: str = Path(..., description="ID of the video to retrieve"),
    current_user: User = Depends(token_required)  # Authenticated user
):
    video = video_service.get_video_by_id(video_id)
    return SuccessResponse(data=video)


@router.delete("/{video_id}", response_model=SuccessResponse[None])
def delete_video(
    video_id: str = Path(..., description="ID of the video to delete"),
    current_user: User = Depends(token_required)  # Authenticated user
):
    video_service.delete_video(video_id)
    return SuccessResponse(data=None)


@router.put("/{video_id}", response_model=SuccessResponse[VideoDTO])
async def edit_video(
    data: EditVideoRequest,  # Request body with edit details
    video_id: str = Path(..., description="ID of the video to update"),
    current_user: User = Depends(token_required)  # Authenticated user
):
    video = await video_service.edit_video(
        creator=current_user,
        video_id=video_id,
        **data.model_dump(exclude_none=True, by_alias=True)
    )
    return SuccessResponse(data=video)


"""
@router.get("/", response_model=SuccessResponse[list[VideoDTO]])
def list_all_videos(
    creator_id: str = Query(None, description="Filter by creator's user ID"),
    title: str = Query(None, description="Filter by video title"),
    topic: str = Query(None, description="Filter by video topic"),
    sort: str = Query("-created_at", description="Sort order, e.g. -created_at or title"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of videos to return"),
    current_user: dict = Depends(token_required)  # Authenticated user
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
"""