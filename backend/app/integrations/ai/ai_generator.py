from typing import List
from app.models import Video

class AIGenerator:
    @staticmethod
    async def generate_topic_suggestions(keyword: str, limit: int) -> List[str]:
        if not keyword:
            # Mock general topics
            return [f"Suggestion trend {i}" for i in range(1, limit + 1)]
        
        # Mock topic suggestions based on query
        return [f"{keyword} trend {i}" for i in range(1, limit + 1)]

    @staticmethod
    async def generate_trending_topics(limit: int) -> List[str]:
        # Mock trending topics
        return ["Tech 2025", "AI Tutorial", "Short Video Trends"]

    @staticmethod
    async def generate_script(topic: str) -> str:
        # Mock script
        return f"Đây là đoạn script mô phỏng từ chủ đề: '{topic}'. Nội dung chi tiết sẽ do AI tạo ra sau."

    @staticmethod
    async def generate_voice(script: str) -> str:
        # TODO

        # Actually returns the raw TTS audio URL from cloud providers (e.g., Play.ht, ElevenLabs, etc.)
        # Mock audio URL
        return "https://res.cloudinary.com/df8meqyyc/video/upload/v1750279229/skanews_pyv1gd.mp3"

    @staticmethod
    async def generate_background_image(topic: str) -> str:
        # TODO

        # Mock background image URL
        return "https://res.cloudinary.com/df8meqyyc/image/upload/v1750280031/tech2025_hgsl68.jpg"

    @staticmethod
    async def generate_video(video: Video) -> str:
        # TODO

        # Mock video URL
        return "https://res.cloudinary.com/df8meqyyc/video/upload/v1750280402/text-to-video_rmp4vx.mp4"