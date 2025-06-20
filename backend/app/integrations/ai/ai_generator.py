from typing import List
from app.models import Video

class AIGenerator:
    @staticmethod
    async def generate_topic_suggestions(query: str) -> List[str]:
        if not query:
            return ["General topic 1", "General topic 2", "General topic 3"]  # Mock general topics
        return [f"{query} trend {i}" for i in range(1, 4)]  # Mock topic suggestions based on query

    @staticmethod
    async def generate_trending_topics() -> List[str]:
        return ["Tech 2025", "AI Tutorial", "Short Video Trends"]  # Mock trending topics

    @staticmethod
    async def generate_script(topic: str) -> str:
        return f"Đây là đoạn script mô phỏng từ chủ đề: '{topic}'. Nội dung chi tiết sẽ do AI tạo ra sau."  # Mock script

    @staticmethod
    async def generate_voice(script: str) -> str:
        return "https://res.cloudinary.com/df8meqyyc/video/upload/v1750279229/skanews_pyv1gd.mp3"  # Mock URL

    @staticmethod
    async def generate_background_image(topic: str) -> str:
        return "https://res.cloudinary.com/df8meqyyc/image/upload/v1750280031/tech2025_hgsl68.jpg"  # Mock URL

    @staticmethod
    async def generate_video(video: Video) -> str:
        return "https://res.cloudinary.com/df8meqyyc/video/upload/v1750280402/text-to-video_rmp4vx.mp4"  # Mock URL