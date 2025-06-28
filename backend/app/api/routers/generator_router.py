from fastapi import APIRouter, Depends, Query
from typing import List
from app.models import User
from app.dtos import VideoDTO
from app.services import GeneratorService
from app.api.middlewares import token_required
from app.schemas.responses import SuccessResponse
from app.schemas.requests import (
    GenerateScriptRequest,
    RegenerateScriptRequest,
    GenerateVoiceRequest,
    GenerateVideoRequest
)

router = APIRouter(prefix="/api/generators", tags=["generators"])


@router.get("/topic/suggestions", response_model=SuccessResponse[List[str]])
async def get_suggested_topics(
    keyword: str = Query("", description="Keyword to filter topic suggestions"),
    limit: int = Query(5, ge=1, le=50, description="Maximum number of suggestions to return"),
    current_user: User = Depends(token_required)
):
    suggestions = await GeneratorService.get_suggested_topics(keyword, limit)
    return SuccessResponse(data=suggestions)


@router.get("/topic/trending", response_model=SuccessResponse[List[str]])
async def get_trending_topics(
    limit: int = Query(5, ge=1, le=20, description="Maximum number of suggestions to return"),
    current_user: User = Depends(token_required)
):
    trending = await GeneratorService.get_trending_topics(limit)
    return SuccessResponse(data=trending)


@router.post("/script", response_model=SuccessResponse[VideoDTO])
async def generate_script(data: GenerateScriptRequest, current_user: User = Depends(token_required)):
    video = await GeneratorService.generate_script(data.topic, current_user)
    return SuccessResponse(data=video)


@router.post("/script/regenerate", response_model=SuccessResponse[VideoDTO])
async def regenerate_script(data: RegenerateScriptRequest, current_user: User = Depends(token_required)):
    video = await GeneratorService.regenerate_script(data.video_id)
    return SuccessResponse(data=video)


@router.post("/voice", response_model=SuccessResponse[VideoDTO])
async def generate_voice(data: GenerateVoiceRequest, current_user: dict = Depends(token_required)):
    video = await GeneratorService.generate_voice(data.video_id, data.script, current_user)
    return SuccessResponse(data=video)


@router.post("/video", response_model=SuccessResponse[VideoDTO])
async def generate_video(data: GenerateVideoRequest, current_user: User = Depends(token_required)):
    video = await GeneratorService.generate_video(data.video_id, str(current_user.id))
    return SuccessResponse(data=video)