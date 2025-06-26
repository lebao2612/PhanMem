from typing import List
from app.repository import VideoRepository
from app.models import MediaInfo, User, Video
from app.dtos import VideoDTO
from app.exceptions import HandledException
from app.integrations import AIGenerator, CloudinaryClient

class GeneratorService:
    @staticmethod
    async def get_suggested_topics(keyword: str, limit: int) -> List[str]:
        # Generate topic suggestions (based on a keyword).
        return await AIGenerator.generate_topic_suggestions(keyword, limit)

    @staticmethod
    async def get_trending_topics(limit: int) -> List[str]:
        # Generate trending topics.
        return await AIGenerator.generate_trending_topics(limit)

    @staticmethod
    async def generate_script(topic: str) -> str:
        # Generate a script based on the topic.
        if not topic:
            raise HandledException("Topic must not empty", 400)
        return await AIGenerator.generate_script(topic)

    @staticmethod
    async def generate_voice(topic: str, script: str, creator: User) -> VideoDTO:
        # Generate voice audio from script and create a draft video entry.
        audio_bytes = await AIGenerator.generate_voice(script)

        # Upload generated audio to Cloudinary (as video resource type).
        public_id, url = await CloudinaryClient.upload_bytes(
            data=audio_bytes,
            resource_type="video",  # Cloudinary treats mp3 as video
            folder="tts-audio"
        )

        # Create MediaInfo object for the uploaded audio.
        voice = MediaInfo(public_id=public_id, url=url)

        # Prepare video data and create a draft video entry in the repository.
        data = {
            "topic": topic,
            "script": script,
            "creator": creator,
            "voice": voice,
            "status": "draft"
        }
        video = VideoRepository.create_video(data)

        # Return the created video as a DTO.
        return VideoDTO.from_model(video)

    @staticmethod
    async def generate_video(video_id: str, creator_id: str) -> VideoDTO:
        # Generate a video
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        if str(video.creator.id) != creator_id:
            raise HandledException("Không có quyền thực hiện", 403)
        if not video.voice:
            raise HandledException("Audio không tồn tại", 400)
        
        VideoRepository.update_status(video, "processing")
        video_url = await AIGenerator.generate_video(video)
        
        video.video = MediaInfo(public_id="mock_video_id", url=video_url)
        VideoRepository.update_status(video, "done")
        
        return VideoDTO.from_model(video)