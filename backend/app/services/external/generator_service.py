import asyncio
import os
import uuid
import tempfile
from app.models import User, Video, ImageMedia, VoiceMedia
from app.exceptions import HandledException
from app.repositories import VideoRepository
from app.dtos import (
    MediaDTO,
    VideoDTO,VideoSceneDTO,
    YoutubeVideoMetadataDTO,
)
from app.integrations import (
    CloudinaryClient,
    GeminiClient,
    GoogleTTSClient,
    StableDiffusionClient
)
from app.utils import time_util
from app.module import render_video

class GeneratorService:
    def __init__(
        self,
        video_repo: VideoRepository,
        gemini_client: GeminiClient,
        google_tts_client: GoogleTTSClient,
        cloudinary_client: CloudinaryClient,
        stable_diffusion_client: StableDiffusionClient
    ):
        self.video_repo = video_repo
        self.gemini_client = gemini_client
        self.google_tts_client = google_tts_client
        self.cloudinary_client = cloudinary_client
        self.stable_diffusion_client = stable_diffusion_client

    async def get_suggested_topics(
        self,
        creator: User,
        keyword: str, limit: int,
        model_name:str = None,
        language: str = None,
    ) -> list[str]:
        if not model_name and creator and creator.settings:
            model_name = creator.settings.llm_model
        if not language and creator and creator.settings:
            language = creator.settings.language
        
        try:     
            return await self.gemini_client.generate_suggested_topics(
                keyword=keyword,
                limit=limit,
                model_name=model_name,
                language=language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi lấy suggested topics: {e}") from e

    async def get_trending_topics(
        self,
        creator: User,
        limit: int,
        model_name:str = None,
        language: str = None,
    ) -> list[str]:
        if not model_name and creator and creator.settings:
            model_name = creator.settings.llm_model
        if not language and creator and creator.settings:
            language = creator.settings.language
        
        try:
            return await self.gemini_client.generate_trending_topics(
                limit=limit,
                model_name=model_name,
                language=language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi lấy trending topics: {e}") from e

    async def generate_script(
        self,
        creator: User,
        topic: str,
        language: str=None,
        model_name: str=None,
        scene_count: int=5
    ) -> list[VideoSceneDTO]:
        if not topic:
            raise HandledException("Topic must not be empty", 400)
        if not model_name and creator and creator.settings:
            model_name = creator.settings.llm_model
        if not language and creator and creator.settings:
            language = creator.settings.language
        
        try:
            scenes = await self.gemini_client.generate_script(
                topic=topic,
                model_name=model_name,
                language=language,
                scene_count=scene_count
            )
            return [VideoSceneDTO(label=scene["label"], subtitle=scene["subtitle"]) for scene in scenes]
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo script: {e}") from e

    async def generate_voices(
        self,
        creator: User,
        subtitles: list[str],
        voice_gender: str=None,
        voice_language: str=None,
    ) -> list[MediaDTO]:
        if not voice_gender and creator.settings:
            voice_gender = creator.settings.voice_gender
        if not voice_language and creator.settings:
            voice_language = creator.settings.language

        async def process_subvoice(index: int, sub: str) -> VoiceMedia:
            try:
                # 1. Generate voice
                audio_data = await self.google_tts_client.generate_voice(
                    subtitle=sub,
                    voice_gender=voice_gender,
                    language=voice_language
                )

                # 2. Upload voice
                upload_result = self.cloudinary_client.upload_from_bytes(
                    data=audio_data,
                    resource_type="video",  # Cloudinary accepts mp3 as video
                    folder=f"{creator.id}/{time_util.datetime_to_str(dt=time_util.datetime_now())}/voices",
                )

                return MediaDTO(
                    url=upload_result["url"],
                    public_id=upload_result["public_id"],
                )
            except Exception as e:
                raise HandledException(f"Lỗi xử lý voice cho subtitle #{index + 1}: {e}", 400) from e

        try:
            tasks = [
                process_subvoice(i, sub)
                for i, sub in enumerate(subtitles)
            ]
            return await asyncio.gather(*tasks)
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo hoặc tải voice: {e}", 400) from e

    async def generate_images(
        self,
        creator: User,
        labels: list[str]
    ) -> list[MediaDTO]:
        if not labels:
            raise HandledException("Label list is empty", 400)

        async def process_image(index: int, label: str) -> MediaDTO:
            try:
                # 1. Generate image từ label
                image_url = await self.stable_diffusion_client.generate_image(label=label)

                # 2. Upload image từ URL lên Cloudinary
                upload_result = self.cloudinary_client.upload_from_url(
                    image_url,
                    resource_type="image",
                    folder=f"{creator.id}/{time_util.datetime_to_str(dt=time_util.datetime_now())}/images",
                )

                return MediaDTO(
                    url=upload_result["url"],
                    public_id=upload_result["public_id"]
                )
            except Exception as e:
                raise HandledException(f"Lỗi xử lý image #{index + 1}: {e}", 400) from e

        try:
            tasks = [process_image(i, label) for i, label in enumerate(labels)]
            return await asyncio.gather(*tasks)
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo hoặc tải ảnh: {e}", 400) from e

    async def generate_video(
        self,
        creator: User,
        title: str,
        topic: str,
        scenes: list[dict],
    ) -> VideoDTO:
        if not scenes or not topic or not creator:
            raise HandledException(f"Lỗi khi tạo video: Thiếu thông tin", 400)
        
        try:
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            tmp_file.close()

            await render_video(scenes=scenes, output_path=tmp_file.name, suffix=".mp4")
            
            upload_result = self.cloudinary_client.upload_from_path(
                file_path=tmp_file.name,
                resource_type="video",
                folder=f"{creator.id}/{time_util.datetime_to_str(dt=time_util.datetime_now())}/video",
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo mới video: {e}", 500) from e
        finally:
            if os.path.exists(tmp_file.name):
                os.remove(tmp_file.name)

        try:
            video = self.video_repo.create_video(
                creator=creator,
                topic=topic,
                scenes=scenes,
                src=upload_result,
                title=title
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi lưu video xuống database: {e}", 500) from e
        
        return VideoDTO.from_model(video=video)
