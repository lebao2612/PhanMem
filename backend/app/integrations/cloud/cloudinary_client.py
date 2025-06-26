from io import BytesIO
import uuid
import httpx
import cloudinary
import cloudinary.uploader
from config import settings
from app.services import HandledException

# Cấu hình Cloudinary khi khởi động
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


class CloudinaryClient:
    @staticmethod
    async def upload_bytes(data: bytes, resource_type: str = "auto", folder: str = "uploads") -> tuple[str, str]:
        try:
            public_id = f"{folder}/{uuid.uuid4().hex}"
            result = cloudinary.uploader.upload(
                BytesIO(data),
                resource_type=resource_type,
                folder=folder,
                public_id=public_id.split("/")[-1]  # chỉ tên file, không bao gồm folder
            )
            return result["public_id"], result["secure_url"]

        except Exception as e:
            raise HandledException(status_code=500, detail=f"Upload to Cloudinary failed: {e}")

    @staticmethod
    async def download_file(url: str) -> bytes:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Tải file thất bại: {e}")
    
    @staticmethod
    async def delete_file(public_id: str, resource_type: str = "image") -> bool:
        """
        Xoá file khỏi Cloudinary dựa trên public_id.
        public_id chỉ là tên file (không chứa folder).
        """
        try:
            result = cloudinary.uploader.destroy(
                public_id=public_id,
                resource_type=resource_type
            )
            # Kết quả có dạng: {'result': 'ok'} nếu xóa thành công
            return result.get("result") == "ok"

        except Exception as e:
            raise HandledException(status_code=500, detail=f"Xoá file thất bại: {e}")
