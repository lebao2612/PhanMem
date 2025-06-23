from typing import List
from app.repository import VideoRepository
from app.models import MediaInfo
from app.dtos import VideoDTO
from app.exceptions import HandledException
from app.integrations.ai.ai_generator import AIGenerator

class GeneratorService:
    @staticmethod
    async def get_suggestions(query: str) -> List[str]:
        """
        Lấy gợi ý topic từ query.
        """
        return await AIGenerator.generate_topic_suggestions(query)

    @staticmethod
    async def get_trending() -> List[str]:
        """
        Lấy danh sách topic trending.
        """
        return await AIGenerator.generate_trending_topics()

    @staticmethod
    async def generate_script_from_topic(topic: str) -> str:
        """
        Sinh script từ topic.
        """
        if not topic:
            raise HandledException("Chủ đề không được để trống", 400)
        return await AIGenerator.generate_script(topic)

    @staticmethod
    async def generate_voice(video_id: str, creator_id: str) -> VideoDTO:
        """
        Sinh voice cho video từ script.
        """
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        if str(video.creator.id) != creator_id:
            raise HandledException("Không có quyền thực hiện", 403)
        if not video.script:
            raise HandledException("Script không tồn tại", 400)
        voice_url = await AIGenerator.generate_voice(video.script)
        video.audio = MediaInfo(public_id="mock_audio_id", url=voice_url)
        VideoRepository.update_status(video, "processing")
        return VideoDTO.from_model(video)

    @staticmethod
    async def generate_video(video_id: str, creator_id: str) -> VideoDTO:
        """
        Sinh video hoàn chỉnh, tự động sinh ảnh nền từ topic.
        """
        video = VideoRepository.find_by_id(video_id)
        if not video:
            raise HandledException("Video không tồn tại", 404)
        if str(video.creator.id) != creator_id:
            raise HandledException("Không có quyền thực hiện", 403)
        if not video.audio:
            raise HandledException("Audio không tồn tại", 400)
        video_url = await AIGenerator.generate_video(video)
        video.video = MediaInfo(public_id="mock_video_id", url=video_url)
        VideoRepository.update_status(video, "done")
        return VideoDTO.from_model(video)