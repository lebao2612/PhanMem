from io import BytesIO
import uuid
import cloudinary
import cloudinary.uploader
from config import settings
from app.exceptions import HandledException

# Cấu hình Cloudinary khi khởi động
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


class CloudinaryClient:
    @staticmethod
    async def upload_file(data: bytes, resource_type: str = "auto", folder: str = "uploads") -> dict:
        """Upload dữ liệu bytes lên Cloudinary"""
        try:
            public_id = f"{folder}/{uuid.uuid4().hex}"
            result = cloudinary.uploader.upload(
                BytesIO(data),
                resource_type=resource_type,
                folder=folder,
                public_id=public_id.split("/")[-1]
            )
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "format": result["format"],
                "size": result.get("bytes", 0)
            }
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Upload to Cloudinary failed: {e}")

    @staticmethod
    async def delete_file(public_id: str, resource_type: str = "auto") -> bool:
        """Xoá file khỏi Cloudinary dựa vào public_id"""
        try:
            result = cloudinary.uploader.destroy(
                public_id=public_id,
                resource_type=resource_type
            )
            return result.get("result") == "ok"
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Xoá file thất bại: {e}")

    @staticmethod
    def get_file_url(public_id: str, resource_type: str = "auto") -> str:
        """Tạo secure URL từ public_id"""
        try:
            return cloudinary.CloudinaryImage(public_id).build_url(
                resource_type=resource_type,
                secure=True
            )
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Lấy URL thất bại: {e}")
