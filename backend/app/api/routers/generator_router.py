from fastapi import APIRouter, Depends, Query
from app.models import User
from app.dependencies import generator_service
from app.api.middlewares import token_required
from app.schemas.responses import SuccessResponse
from app.schemas.requests import (
    GenerateScriptRequest,
    GenerateVoicesRequest,
    GenerateVideoRequest,
    GenerateImagesRequest
)
from app.dtos import (
    MediaDTO,
    VideoDTO, VideoSceneDTO,
    YoutubeVideoMetadataDTO
)

router = APIRouter(prefix="/api/generators", tags=["generators"])


@router.get("/topic/suggestions", response_model=SuccessResponse[list[str]])
async def get_suggested_topics(
    keyword: str = Query("", description="Keyword to filter topic suggestions"),
    limit: int = Query(5, ge=1, le=50, description="Maximum number of suggestions to return"),
    model_name: str = Query("gemini-1.5-flash", description="LLM model name"),
    language: str = Query("vi", description="Language"),
    current_user: User = Depends(token_required)
):
    suggestions = await generator_service.get_suggested_topics(
        creator=current_user,
        keyword=keyword,
        limit=limit,
        model_name=model_name,
        language=language
    )
    return SuccessResponse(data=suggestions)


@router.get("/topic/trending", response_model=SuccessResponse[list[str]])
async def get_trending_topics(
    limit: int = Query(5, ge=1, le=20, description="Maximum number of suggestions to return"),
    model_name: str = Query("gemini-1.5-flash", description="LLM model name"),
    language: str = Query("vi", description="Language"),
    current_user: User = Depends(token_required)
):
    trending = await generator_service.get_trending_topics(
        creator=current_user,
        limit=limit,
        model_name=model_name,
        language=language
    )
    return SuccessResponse(data=trending)


@router.post("/script", response_model=SuccessResponse[list[VideoSceneDTO]])
async def generate_script(data: GenerateScriptRequest, current_user: User = Depends(token_required)):
    video = await generator_service.generate_script(
        creator=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True)
        # topic=data.topic,
        # model_name=data.model_name,
        # language=data.language,
        # scene_count=data.scene_count
    )
    return SuccessResponse(data=video)


@router.post("/voices", response_model=SuccessResponse[list[MediaDTO]])
async def generate_voices(data: GenerateVoicesRequest, current_user: User = Depends(token_required)):
    video = await generator_service.generate_voices(
        creator=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True)
        # subtitles=data.subtitles,
        # voice_gender=data.voice_gender,
        # voice_language=data.voice_language,
    )
    return SuccessResponse(data=video)

@router.post("/images", response_model=SuccessResponse[list[MediaDTO]])
async def generate_image(data: GenerateImagesRequest, current_user: User = Depends(token_required)):
    video = await generator_service.generate_images(
        creator=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True),
        # labels=data.labels,
    )
    return SuccessResponse(data=video)

@router.post("/video", response_model=SuccessResponse[VideoDTO])
async def generate_video(data: GenerateVideoRequest, current_user: User = Depends(token_required)):
    video = await generator_service.generate_video(
        creator=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True),
        # title=data.title,
        # topic=data.topic,
        # scenes=data.scenes,
    )
    return SuccessResponse(data=video)