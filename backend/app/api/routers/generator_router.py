from fastapi import APIRouter, Depends, Query, File, UploadFile
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
    current_user: User = Depends(token_required)
):
    suggestions = await generator_service.get_suggested_topics(
        creator=current_user,
        keyword=keyword,
        limit=limit,
    )
    return SuccessResponse(data=suggestions)

@router.get("/topic/trending", response_model=SuccessResponse[list[str]])
async def get_trending_topics(
    limit: int = Query(5, ge=1, le=20, description="Maximum number of suggestions to return"),
    current_user: User = Depends(token_required)
):
    trending = await generator_service.get_trending_topics(
        creator=current_user,
        limit=limit,
    )
    return SuccessResponse(data=trending)


@router.post("/script", response_model=SuccessResponse[list[VideoSceneDTO]])
async def generate_script(data: GenerateScriptRequest, current_user: User = Depends(token_required)):
    scenes = await generator_service.generate_script(
        creator=current_user,
        topic=data.topic,
        scene_count=data.scene_count
    )
    return SuccessResponse(data=scenes)


@router.post("/voices", response_model=SuccessResponse[list[MediaDTO]])
async def generate_voices(data: GenerateVoicesRequest, current_user: User = Depends(token_required)):
    voices = await generator_service.generate_voices(
        creator=current_user,
        subtitles=data.subtitles,
    )
    return SuccessResponse(data=voices)

@router.patch("/voices", response_model=SuccessResponse[MediaDTO])
async def update_scene_voice(
    public_id: str = Query(..., description="Public ID of the voice file to be replaced"),
    file: UploadFile = File(..., description="New audio file to upload and replace the existing voice"),
    current_user: User = Depends(token_required)
):
    voice_bytes = await file.read()
    result = await generator_service.replace_scene_voice(
        public_id=public_id,
        data=voice_bytes,
    )
    return SuccessResponse(data=result)

@router.post("/images", response_model=SuccessResponse[list[MediaDTO]])
async def generate_image(data: GenerateImagesRequest, current_user: User = Depends(token_required)):
    images = await generator_service.generate_images(
        creator=current_user,
        labels=data.labels,
    )
    return SuccessResponse(data=images)

@router.patch("/images", response_model=SuccessResponse[MediaDTO])
async def update_image(
    public_id: str = Query(..., description="Public ID of the image file to be replaced"),
    file: UploadFile = File(..., description="New audio file to upload and replace the existing voice"),
    current_user: User = Depends(token_required),
):
    image_bytes = await file.read()
    result = await generator_service.replace_scene_image(
        public_id=public_id,
        data=image_bytes,
    )
    return SuccessResponse(data=result)

@router.post("/video", response_model=SuccessResponse[VideoDTO])
async def generate_video(data: GenerateVideoRequest, current_user: User = Depends(token_required)):
    video = await generator_service.generate_video(
        creator=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True),
    )
    return SuccessResponse(data=video)