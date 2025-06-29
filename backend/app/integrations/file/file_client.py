import os
import time
import httpx
from app.exceptions import HandledException


class FileClient:
    @staticmethod
    async def download_to_bytes(url: str) -> bytes:
        """Tải dữ liệu từ URL và trả về dạng bytes"""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Tải file thất bại: {e}")

    @staticmethod
    async def download_to_file(url: str, path: str) -> None:
        """Tải dữ liệu từ URL và lưu vào file local"""
        try:
            data = await FileClient.download_to_bytes(url)
            with open(path, "wb") as f:
                f.write(data)
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Lưu file thất bại: {e}")

    @staticmethod
    def delete_file(path: str) -> None:
        """Xoá file local nếu tồn tại"""
        try:
            if os.path.exists(path):
                time.sleep(1)
                os.remove(path)
        except Exception as e:
            raise HandledException(status_code=500, detail=f"Xoá file thất bại: {e}")
