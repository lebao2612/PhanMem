from app.repositories import VideoRepository
from app.models import User
from app.dtos import VideoDTO
from app.exceptions import HandledException
from app.integrations import CloudinaryClient, GeminiClient, GoogleTTS, StableDiffusionClient
from app.utils import FileUtil


class GeneratorService:
    @staticmethod
    async def get_suggested_topics(
        keyword: str, limit: int,
        creator: User=None) -> list[str]:
        # Generate topic suggestions (based on a keyword).
        return await GeminiClient.generate_suggested_topics(
            keyword=keyword, limit=limit,
            model_name=creator.settings.llm_model,
            language=creator.settings.language
        )

    @staticmethod
    async def get_trending_topics(
        limit: int,
        creator: User=None) -> list[str]:
        # Generate trending topics.
        return await GeminiClient.generate_trending_topics(
            limit=limit,
            model_name=creator.settings.llm_model,
            language=creator.settings.language
        )

    @staticmethod
    async def generate_script(
        topic: str, creator: User,
    ) -> VideoDTO:
        # Generate a script based on the topic.
        if not topic:
            raise HandledException("Topic must not empty", 400)
        
        script = await GeminiClient.generate_script(
            topic=topic,
            language=creator.settings.language,
            model_name=creator.settings.llm_model
        )

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
        
        script = await GeminiClient.generate_script(
            topic=video.topic,
            language=creator.settings.language,
            model_name=creator.settings.llm_model
        )

        video = VideoRepository.update_script(video=video, script=script)
        return VideoDTO.from_model(video)

    @staticmethod
    async def generate_voice(
        video_id: str, creator: User, script: list[dict]) -> VideoDTO:
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video does not exist", 404)
        if str(video.creator.id) != str(creator.id):
            raise HandledException("Permission denied", 403)
        if not video.script:
            raise HandledException("Script does not exist", 404)
        
        # Generate voice audio from script and create a draft video entry.
        subtitles = [scene["subtitle"] for scene in script if "subtitle" in scene]
        audio_chunks = await GoogleTTS.generate_voice(
            subtitles=subtitles,
            gender=creator.settings.voice_gender,
            language=creator.settings.language
        )

        # Get durations and update scripts
        for i, chunk in enumerate(audio_chunks):
            script[i]["duration"] = FileUtil.get_mp3_duration(data=chunk)

        # Merge audio
        final_bytes = FileUtil.merge_mp3_chunks(chunks=audio_chunks)

        # Upload generated audio to Cloudinary (as video resource type).
        upload_res = await CloudinaryClient.upload_file(
            data=final_bytes,
            resource_type="video",  # Cloudinary treats mp3 as video
            folder=f"{creator.id}/{video_id}/voices"
        )
        
        video = VideoRepository.update_voice(
            video=video,
            url=upload_res["url"],
            public_id=upload_res["public_id"],
        )

        video = VideoRepository.update_script(
            video=video,
            script=script
        )

        return VideoDTO.from_model(video)

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
        # video_bytes = await StableDiffusionClient.generate_video(video)

        # TODO: Upload the generated video to Cloudinary
        # public_id, video_url = await CloudinaryClient.upload_bytes(
        #     data=video_bytes,
        #     resource_type="video",
        #     folder=f"{creator_id}/videos"
        # )

        public_id = "mock_video_id"
        video_url = "https://res.cloudinary.com/df8meqyyc/video/upload/v1750280402/text-to-video_rmp4vx.mp4"
        
        video = VideoRepository.update_video(
            video=video,
            url=video_url,
            public_id=public_id,
        )
        VideoRepository.update_status(video=video, status="done")
        
        return VideoDTO.from_model(video)