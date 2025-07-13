from io import BytesIO
import uuid
import asyncio
import cloudinary
import cloudinary.uploader
from typing import Any

class CloudinaryClient:
    def __init__(self, cloud_name: str, api_key: str, api_secret: str):
        try:
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
        except Exception as e:
            raise RuntimeError("Cloudinary configuration error.") from e

    async def _upload_cloud(
        self,
        file: Any,
        resource_type: str = "auto",
        filename: str = None
    ) -> dict:
        try:
            folder = None
            public_id = filename or uuid.uuid4().hex

            # Tách folder nếu filename có dấu "/"
            if filename and '/' in filename:
                parts = filename.rsplit('/', 1)
                folder, public_id = parts[0], parts[1]

            result = await asyncio.to_thread(
                cloudinary.uploader.upload,
                file,
                resource_type=resource_type,
                public_id=public_id,
                folder=folder
            )
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "format": result["format"],
                "size": result.get("bytes", 0)
            }

        except Exception as e:
            raise RuntimeError(f"Error uploading to Cloudinary: {e}") from e

    async def upload_from_bytes(
        self,
        data: bytes,
        resource_type: str = "auto",
        filename: str = None
    ) -> dict:
        return await self._upload_cloud(BytesIO(data), resource_type, filename)

    async def upload_from_path(
        self,
        file_path: str,
        resource_type: str = "auto",
        filename: str = None
    ) -> dict:
        return await self._upload_cloud(file_path, resource_type, filename)

    async def upload_from_url(
        self,
        url: str,
        resource_type: str = "auto",
        filename: str = None
    ) -> dict:
        return await self._upload_cloud(url, resource_type, filename)

    def delete_file(self, public_id: str, resource_type: str = "auto") -> bool:
        try:
            result = cloudinary.uploader.destroy(
                public_id=public_id,
                resource_type=resource_type
            )
            return result.get("result") == "ok"
        except Exception as e:
            raise RuntimeError("Error deleting file from Cloudinary.") from e

    def get_file_url(self, public_id: str, resource_type: str = "auto") -> str:
        try:
            return cloudinary.CloudinaryImage(public_id).build_url(
                resource_type=resource_type,
                secure=True
            )
        except Exception as e:
            raise RuntimeError("Error generating URL from public_id.") from e
