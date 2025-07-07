from fastapi import APIRouter, Depends, Query
from app.models import User
from app.dtos import VideoDTO
from app.dependencies import generator_service
from app.api.middlewares import token_required
from app.schemas.responses import SuccessResponse
from app.schemas.requests import (
    GenerateScriptRequest,
    RegenerateScriptRequest,
    GenerateVoiceRequest,
    GenerateVideoRequest
)

router = APIRouter(prefix="/api/generators", tags=["generators"])


@router.get("/topic/suggestions", response_model=SuccessResponse[list[str]])
async def get_suggested_topics(
    keyword: str = Query("", description="Keyword to filter topic suggestions"),
    limit: int = Query(5, ge=1, le=50, description="Maximum number of suggestions to return"),
    current_user: User = Depends(token_required)
):
    suggestions = await generator_service.get_suggested_topics(
        keyword=keyword,
        limit=limit,
        creator=current_user
    )
    return SuccessResponse(data=suggestions)


@router.get("/topic/trending", response_model=SuccessResponse[list[str]])
async def get_trending_topics(
    limit: int = Query(5, ge=1, le=20, description="Maximum number of suggestions to return"),
    current_user: User = Depends(token_required)
):
    trending = await generator_service.get_trending_topics(
        limit=limit,
        creator=current_user
    )
    return SuccessResponse(data=trending)


@router.post("/script", response_model=SuccessResponse[VideoDTO])
async def generate_script(data: GenerateScriptRequest, current_user: User = Depends(token_required)):
    video = await generator_service.generate_script(
        topic=data.topic,
        creator=current_user
    )
    return SuccessResponse(data=video)


@router.post("/script/regenerate", response_model=SuccessResponse[VideoDTO])
async def regenerate_script(data: RegenerateScriptRequest, current_user: User = Depends(token_required)):
    video = await generator_service.regenerate_script(
        video_id=data.video_id,
        creator=current_user
    )
    return SuccessResponse(data=video)


@router.post("/voice", response_model=SuccessResponse[VideoDTO])
async def generate_voice(data: GenerateVoiceRequest, current_user: dict = Depends(token_required)):
    video = await generator_service.generate_voice(
        video_id=data.video_id,
        creator=current_user,
        script=data.script
    )
    return SuccessResponse(data=video)


@router.post("/video", response_model=SuccessResponse[VideoDTO])
async def generate_video(data: GenerateVideoRequest, current_user: User = Depends(token_required)):
    video = await generator_service.generate_video(
        video_id=data.video_id,
        creator=current_user
    )
    return SuccessResponse(data=video)
