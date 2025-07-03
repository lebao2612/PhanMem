import os, time, io
import httpx
from moviepy import VideoFileClip
import audioread
from app.exceptions import HandledException

class FileUtil:
    @staticmethod
    async def download_to_bytes(url: str) -> bytes:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            raise HandledException(500, f"Tải file thất bại: {e}")

    @staticmethod
    async def download_to_file(url: str, path: str) -> None:
        try:
            data = await FileUtil.download_to_bytes(url)
            with open(path, "wb") as f:
                f.write(data)
        except Exception as e:
            raise HandledException(500, f"Lưu file thất bại: {e}")

    @staticmethod
    def delete_file(path: str) -> None:
        try:
            if os.path.exists(path):
                time.sleep(1)
                os.remove(path)
        except Exception as e:
            raise HandledException(500, f"Xoá file thất bại: {e}")

    # === Audio ===
    @staticmethod
    def get_mp3_duration(data: bytes) -> float:
        try:
            with audioread.audio_open(io.BytesIO(data)) as f:
                return round(f.duration, 2)
        except Exception as e:
            raise HandledException(500, f"Không thể tính thời lượng mp3: {e}")

    @staticmethod
    def merge_mp3_chunks(chunks: list[bytes]) -> bytes:
        try:
            return b"".join(chunks)
        except Exception as e:
            raise HandledException(500, f"Không thể ghép mp3: {e}")

    # === Video ===
    @staticmethod
    def get_mp4_duration(file_path: str) -> float:
        try:
            with VideoFileClip(file_path) as clip:
                return round(clip.duration, 2)
        except Exception as e:
            raise HandledException(500, f"Không thể tính thời lượng mp4: {e}")
