from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.services.generator_service import GeneratorService
from app.dtos import VideoDTO
from app.api.middlewares import token_required
from app.schemas.request.generator import *

router = APIRouter(prefix="/api/generators", tags=["generators"])

@router.get("/topic/suggestions", response_model=List[str])
async def get_suggestions(query: str = Query(""), current_user: dict = Depends(token_required)):
    suggestions = await GeneratorService.get_suggestions(query)
    return suggestions


@router.get("/topic/trending", response_model=List[str])
async def get_trending(current_user: dict = Depends(token_required)):
    trending = await GeneratorService.get_trending()
    return trending


@router.post("/script")
async def generate_script(data: GenerateScriptRequest, current_user: dict = Depends(token_required)):
    script = await GeneratorService.generate_script_from_topic(data.topic)
    return {"topic": data.topic, "script": script}


@router.post("/voice", response_model=VideoDTO)
async def generate_voice(data: GenerateVoiceRequest, current_user: dict = Depends(token_required)):
    video = await GeneratorService.generate_voice(data.video_id, str(current_user["current_user"].id))
    return video


@router.post("/video", response_model=VideoDTO)
async def generate_video(data: GenerateVideoRequest, current_user: dict = Depends(token_required)):
    video = await GeneratorService.generate_video(data.video_id, str(current_user["current_user"].id))
    return video
