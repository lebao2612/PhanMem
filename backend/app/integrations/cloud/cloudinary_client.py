from io import BytesIO
import uuid
import cloudinary
import cloudinary.uploader


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

    def upload_from_bytes(
        self,
        data: bytes,
        resource_type: str = "auto",
        folder: str = "uploads",
        filename: str = None
    ) -> dict:
        try:
            result = cloudinary.uploader.upload(
                BytesIO(data),
                resource_type=resource_type,
                folder=folder,
                public_id=filename or uuid.uuid4().hex
            )
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "format": result["format"],
                "size": result.get("bytes", 0)
            }
        except Exception as e:
            raise RuntimeError("Error uploading bytes to Cloudinary.") from e

    def upload_from_path(
        self,
        file_path: str,
        resource_type: str = "auto",
        folder: str = "uploads",
        filename: str = None
    ) -> dict:
        try:
            result = cloudinary.uploader.upload(
                file_path,
                resource_type=resource_type,
                folder=folder,
                public_id=filename or uuid.uuid4().hex
            )
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "format": result["format"],
                "size": result.get("bytes", 0)
            }
        except Exception as e:
            raise RuntimeError(f"Error uploading file from path: {file_path}") from e

    def upload_from_url(
        self,
        url: str,
        resource_type: str = "auto",
        folder: str = "uploads",
        filename: str = None
    ) -> dict:
        try:
            result = cloudinary.uploader.upload(
                url,
                resource_type=resource_type,
                folder=folder,
                public_id=filename or uuid.uuid4().hex
            )
            return {
                "public_id": result["public_id"],
                "url": result["secure_url"],
                "format": result["format"],
                "size": result.get("bytes", 0)
            }
        except Exception as e:
            raise RuntimeError("Error uploading from URL to Cloudinary.") from e

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
