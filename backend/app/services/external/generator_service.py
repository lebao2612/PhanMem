import asyncio, tempfile
from moviepy import (
    ImageClip, AudioFileClip,
    concatenate_videoclips
)
from app.models import User
from app.dtos import VideoDTO
from app.exceptions import HandledException
from app.repositories import VideoRepository
from app.integrations import (
    CloudinaryClient,
    GeminiClient, GoogleTTS, StableDiffusionClient
)
from app.utils import FileUtil


class GeneratorService:
    @staticmethod
    async def get_suggested_topics(
        keyword: str, limit: int,
        creator: User=None) -> list[str]:
        # Generate topic suggestions (based on a keyword).
        try:
            return await GeminiClient.generate_suggested_topics(
                keyword=keyword, limit=limit,
                model_name=creator.settings.llm_model,
                language=creator.settings.language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi lấy suggested topics: {e}") from e

    @staticmethod
    async def get_trending_topics(
        limit: int,
        creator: User=None) -> list[str]:
        # Generate trending topics.
        try:
            return await GeminiClient.generate_trending_topics(
                limit=limit,
                model_name=creator.settings.llm_model,
                language=creator.settings.language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi lấy suggested topics: {e}") from e

    @staticmethod
    async def generate_script(
        topic: str, creator: User,
    ) -> VideoDTO:
        # Generate a script based on the topic.
        if not topic:
            raise HandledException("Topic must not empty", 400)
        try:
            script = await GeminiClient.generate_script(
                topic=topic,
                language=creator.settings.language,
                model_name=creator.settings.llm_model
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo lại script: {e}") from e

        video = VideoRepository.create_draft_video(
            topic=topic,
            creator=creator
        )
        video = VideoRepository.update_script(video=video, script=script)

        return VideoDTO.from_model(video)

    @staticmethod
    async def regenerate_script(
        video_id: str, creator: User,
    ) -> VideoDTO:
        # Regenerate script for an existing video.
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not video.topic:
            raise HandledException("Topic must not empty", 400)

        try:        
            script = await GeminiClient.generate_script(
                topic=video.topic,
                language=creator.settings.language,
                model_name=creator.settings.llm_model
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi tạo lại script: {e}") from e

        video = VideoRepository.update_script(video=video, script=script)
        return VideoDTO.from_model(video)

    @staticmethod
    async def generate_voice(
        video_id: str, creator: User, script: list[dict]
    ) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not video.script:
            raise HandledException("Script does not exist", 404)

        # 1. Trích subtitle
        subtitles = [scene["subtitle"] for scene in script if "subtitle" in scene]

        # 2. Gọi GoogleTTS generate_voice (song song TTS)
        try:
            audio_chunks = await GoogleTTS.generate_voices(
                subtitles=subtitles,
                gender=creator.settings.voice_gender,
                language=creator.settings.language
            )
        except Exception as e:
            raise HandledException(f"Lỗi khi generator voice: {e}") from e

        # 3. Song song tính duration
        duration_tasks = [
            asyncio.to_thread(FileUtil.get_mp3_duration, chunk)
            for chunk in audio_chunks
        ]
        durations = await asyncio.gather(*duration_tasks)

        # 4. Gán duration vào script
        for i, duration in enumerate(durations):
            script[i]["duration"] = duration

        # 5. Merge audio
        final_bytes = FileUtil.merge_mp3_chunks(audio_chunks)

        # 6. Upload Cloudinary
        upload_res = await CloudinaryClient.upload_byte(
            data=final_bytes,
            resource_type="video",
            folder=f"{creator.id}/{video_id}/voices"
        )

        # 7. Update DB
        video = VideoRepository.update_voice(
            video=video,
            url=upload_res["url"],
            public_id=upload_res["public_id"]
        )
        video = VideoRepository.update_script(video=video, script=script)

        return VideoDTO.from_model(video)

    @staticmethod
    async def generate_images(video_id: str, creator: User) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video not found", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not video.script:
            raise HandledException("No script to generate images for", 400)

        labels = [scene.label for scene in video.script]

        # TODO:
        # image_urls = await StableDiffusionClient.generate_images(labels)
        raise NotImplementedError("Not implement")

    @staticmethod
    async def generate_video(video_id: str, creator: User) -> VideoDTO:
        # Generate a video
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if video.creator.id != creator.id:
            raise HandledException("Permission denied", 403)
        if not video.voice_file:
            raise HandledException("Voice does not exist", 400)

        # TODO: Gen video
        # labels = [scene.label for scene in video.script]        
        # video_bytes = await ...

        # TODO: Upload the generated video to Cloudinary
        # public_id, video_url = await CloudinaryClient.upload_bytes(
        #     data=video_bytes,
        #     resource_type="video",
        #     folder=f"{creator_id}/videos"
        # )

        # TODO:
        # video = VideoRepository.update_video(
        #     video=video,
        #     url=video_url,
        #     public_id=public_id,
        # )
        # VideoRepository.update_status(video=video, status="done")
        
        videoDTO = VideoDTO.from_model(video)
        videoDTO.video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
        return videoDTO
  