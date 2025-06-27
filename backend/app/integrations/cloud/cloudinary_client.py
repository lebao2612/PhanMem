import cloudinary
import cloudinary.uploader
from app.services import HandledException
from config import settings

class CloudinaryClient:
    @staticmethod
    async def upload_audio(raw_url: str) -> tuple[str, str]:
        """
        Upload audio file to Cloudinary and return public ID and URL.
        """
        return "mock_public_id", "https://res.cloudinary.com/df8meqyyc/video/upload/v1750279229/skanews_pyv1gd.mp3"

    @staticmethod
    async def upload_video(raw_url: str) -> tuple[str, str]:
        """
        Upload audio file to Cloudinary and return public ID and URL.
        """
        return "mock_public_id", "https://res.cloudinary.com/df8meqyyc/video/upload/v1750280402/text-to-video_rmp4vx.mp4"
    
    @staticmethod
    async def upload_image(raw_url: str) -> tuple[str, str]:
        """
        Upload image file to Cloudinary and return public ID and URL.
        """
        return "mock_public_id", "https://res.cloudinary.com/df8meqyyc/image/upload/v1750280031/tech2025_hgsl68.jpg"
    