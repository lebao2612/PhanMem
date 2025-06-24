from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.models import User
from app.dtos import VideoDTO
from app.services import GeneratorService, VideoService
from app.api.middlewares import token_required
from app.schemas.request.generator import *

router = APIRouter(prefix="/api/generators", tags=["generators"])

@router.get("/topic/suggestions", response_model=List[str])
async def get_suggested_topics(
    keyword = Query("", description="Keyword to filter topic suggestions"),
    limit: int = Query(5, ge=1, le=50, description="Maximum number of suggestions to return"),
    current_user: User = Depends(token_required)
    ):
    suggestions = await GeneratorService.get_suggested_topics(keyword, limit)
    return suggestions


@router.get("/topic/trending", response_model=List[str])
async def get_trending_topics(
    limit: int = Query(5, ge=1, le=20, description="Maximum number of suggestions to return"),
    current_user: User = Depends(token_required)
    ):
    trending = await GeneratorService.get_trending_topics(limit)
    return trending


@router.post("/script")
async def generate_script(data: GenerateScriptRequest, current_user: User = Depends(token_required)):
    script = await GeneratorService.generate_script(data.topic)
    return script


@router.post("/voice", response_model=VideoDTO)
async def generate_voice(data: GenerateVoiceRequest, current_user: User = Depends(token_required)):
    video = await GeneratorService.generate_voice(
        title=data.title or "Untitled Video",
        topic=data.topic,
        script=data.script,
        creator=current_user,
        tags=data.tags or []
    )
    return video


@router.post("/video", response_model=VideoDTO)
async def generate_video(data: GenerateVideoRequest, current_user: User = Depends(token_required)):
    video = await GeneratorService.generate_video(data.video_id, str(current_user.id))
    return video
