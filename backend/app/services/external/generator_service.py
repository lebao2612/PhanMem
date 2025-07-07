import asyncio
from app.models import User
from app.dtos import VideoDTO
from app.exceptions import HandledException
from app.repositories import VideoRepository
from app.integrations import (
    CloudinaryClient,
    GeminiClient,
    GoogleTTSClient,
    StableDiffusionClient
)
from app.utils import FileUtil


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

    async def get_suggested_topics(self, keyword: str, limit: int, creator: User = None) -> list[str]:
        try:
            return await self.gemini_client.generate_suggested_topics(
                keyword=keyword,
                limit=limit,
                model_name=creator.settings.llm_model,
                language=creator.settings.language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi lấy suggested topics: {e}") from e

    async def get_trending_topics(self, limit: int, creator: User = None) -> list[str]:
        try:
            return await self.gemini_client.generate_trending_topics(
                limit=limit,
                model_name=creator.settings.llm_model,
                language=creator.settings.language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi lấy trending topics: {e}") from e

    async def generate_script(self, topic: str, creator: User) -> VideoDTO:
        if not topic:
            raise HandledException("Topic must not be empty", 400)
        try:
            script = await self.gemini_client.generate_script(
                topic=topic,
                language=creator.settings.language,
                model_name=creator.settings.llm_model
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo script: {e}") from e

        video = self.video_repo.create_draft_video(topic=topic, creator=creator)
        video = self.video_repo.update_script(video=video, script=script)
        return VideoDTO.from_model(video)

    async def regenerate_script(self, video_id: str, creator: User) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not video.topic:
            raise HandledException("Topic must not be empty", 400)

        try:
            script = await self.gemini_client.generate_script(
                topic=video.topic,
                language=creator.settings.language,
                model_name=creator.settings.llm_model
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo lại script: {e}") from e

        video = self.video_repo.update_script(video=video, script=script)
        return VideoDTO.from_model(video)

    async def generate_voice(self, video_id: str, creator: User, script: list[dict]) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not video.script:
            raise HandledException("Script does not exist", 404)

        subtitles = [scene["subtitle"] for scene in script if "subtitle" in scene]

        try:
            audio_chunks = await self.google_tts_client.generate_voices(
                subtitles=subtitles,
                gender=creator.settings.voice_gender,
                language=creator.settings.language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo voice: {e}") from e

        duration_tasks = [
            asyncio.to_thread(FileUtil.get_mp3_duration, chunk)
            for chunk in audio_chunks
        ]
        durations = await asyncio.gather(*duration_tasks)

        for i, duration in enumerate(durations):
            script[i]["duration"] = duration

        final_bytes = FileUtil.merge_mp3_chunks(audio_chunks)

        upload_res = await self.cloudinary_client.upload_byte(
            data=final_bytes,
            resource_type="video",
            folder=f"{creator.id}/{video_id}/voices"
        )

        video = self.video_repo.update_voice(
            video=video,
            url=upload_res["url"],
            public_id=upload_res["public_id"]
        )
        video = self.video_repo.update_script(video=video, script=script)

        return VideoDTO.from_model(video)

    async def generate_images(self, video_id: str, creator: User) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video not found", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not video.script:
            raise HandledException("No script to generate images for", 400)

        labels = [scene["label"] for scene in video.script]
        # TODO: Chưa implement thật sự
        raise NotImplementedError("Not implemented")

    async def generate_video(self, video_id: str, creator: User) -> VideoDTO:
        video = self.video_repo.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if video.creator.id != creator.id:
            raise HandledException("Permission denied", 403)
        if not video.voice_file:
            raise HandledException("Voice does not exist", 400)

        # TODO: Add logic to generate final video + upload

        videoDTO = VideoDTO.from_model(video)
        videoDTO.video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
        return videoDTO
