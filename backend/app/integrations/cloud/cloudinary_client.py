import cloudinary
import cloudinary.uploader
from app.services import HandledException
from config import settings

class CloudinaryClient:
    @staticmethod
    def init():
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    @staticmethod
    def upload_image(image_data: bytes, folder: str = "images") -> dict:
        try:
            response = cloudinary.uploader.upload(
                image_data, resource_type="image", folder=folder
            )
            return {"public_id": response["public_id"], "url": response["secure_url"]}
        except Exception as e:
            raise HandledException(f"Lỗi tải ảnh: {str(e)}", 500)

    @staticmethod
    def upload_video(video_data: bytes, folder: str = "videos") -> dict:
        try:
            response = cloudinary.uploader.upload(
                video_data, resource_type="video", folder=folder
            )
            return {"public_id": response["public_id"], "url": response["secure_url"]}
        except Exception as e:
            raise HandledException(f"Lỗi tải video: {str(e)}", 500)

    @staticmethod
    def delete_asset(public_id: str, resource_type: str = "image"):
        try:
            cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        except Exception as e:
            raise HandledException(f"Lỗi xóa tài nguyên: {str(e)}", 500)