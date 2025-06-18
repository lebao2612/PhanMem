from typing import List
from app.models import Video

class AIGenerator:
    @staticmethod
    def generate_topic_suggestions(query: str) -> List[str]:
        """
        Sinh gợi ý topic từ query. Mock: Trả danh sách giả.
        Tương lai: Dùng GPT/Claude/DeepSeek với prompt dựa trên query.
        """
        if not query:
            return ["General topic 1", "General topic 2", "General topic 3"] # Mock general topics
        return [f"{query} trend {i}" for i in range(1, 4)] # Mock topic suggestions based on query

    @staticmethod
    def generate_trending_topics() -> List[str]:
        """
        Sinh danh sách topic trending. Mock: Trả danh sách giả.
        Tương lai: Dùng GPT/Claude hoặc API phân tích trend (e.g., X API).
        """
        return ["Tech 2025", "AI Tutorial", "Short Video Trends"] # Mock trending topics

    @staticmethod
    def generate_script(topic: str) -> str:
        """
        Sinh script từ topic. Mock: Trả string giả.
        Tương lai: Dùng GPT/Claude/DeepSeek.
        """
        return f"Đây là đoạn script mô phỏng từ chủ đề: '{topic}'. Nội dung chi tiết sẽ do AI tạo ra sau." # Mock script

    @staticmethod
    def generate_voice(script: str) -> str:
        """
        Sinh voice từ script. Mock: Trả URL giả.
        Tương lai: Dùng Play.ht/ElevenLabs/Bark.
        """
        return "https://res.cloudinary.com/df8meqyyc/video/upload/v1750279229/skanews_pyv1gd.mp3" # Mock URL

    @staticmethod
    def generate_background_image(topic: str) -> str:
        """
        Sinh ảnh nền từ topic. Mock: Trả URL giả.
        Tương lai: Dùng DALL·E/Stable Diffusion/Midjourney.
        """
        return "https://res.cloudinary.com/df8meqyyc/image/upload/v1750280031/tech2025_hgsl68.jpg"  # Mock URL

    @staticmethod
    def generate_video(video: Video) -> str:
        """
        Sinh video từ Video object (chứa script, audio, topic).
        Tự sinh ảnh nền từ topic và ghép với audio.
        Mock: Trả URL giả.
        Tương lai: Dùng MoviePy/RunwayML/Synthesia.
        """
        if not video.audio or not video.audio.url:
            raise ValueError("Video phải có audio")
        if not video.topic:
            raise ValueError("Video phải có topic")
        image_url = AIGenerator.generate_background_image(video.topic)
        # Mock: Ghép audio + ảnh nền
        return "https://res.cloudinary.com/df8meqyyc/video/upload/v1750280402/text-to-video_rmp4vx.mp4" # Mock URL