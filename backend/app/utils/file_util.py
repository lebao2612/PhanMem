import os
import time
import io
import httpx
import audioread


class FileUtil:
    @staticmethod
    async def download_to_bytes(url: str) -> bytes:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except httpx.RequestError as e:
            raise ConnectionError(f"Lỗi kết nối khi tải file: {e}") from e
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Yêu cầu HTTP thất bại: {e.response.status_code}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định khi tải file: {e}") from e

    @staticmethod
    async def download_to_file(url: str, path: str) -> None:
        try:
            data = await FileUtil.download_to_bytes(url)
            with open(path, "wb") as f:
                f.write(data)
        except (IOError, OSError) as e:
            raise IOError(f"Lỗi khi ghi file: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định khi lưu file: {e}") from e

    @staticmethod
    def delete_file(path: str) -> None:
        try:
            if os.path.exists(path):
                time.sleep(1)
                os.remove(path)
        except PermissionError as e:
            raise PermissionError(f"Không có quyền xoá file: {e}") from e
        except (IOError, OSError) as e:
            raise OSError(f"Lỗi hệ thống khi xoá file: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định khi xoá file: {e}") from e

    @staticmethod
    def get_mp3_duration(data: bytes) -> float:
        try:
            with audioread.audio_open(io.BytesIO(data)) as f:
                return round(f.duration, 2)
        except audioread.DecodeError as e:
            raise RuntimeError("Lỗi định dạng hoặc codec khi đọc MP3") from e
        except IOError as e:
            raise IOError(f"Lỗi khi đọc MP3: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định khi tính thời lượng MP3: {e}") from e

    @staticmethod
    def merge_mp3_chunks(chunks: list[bytes]) -> bytes:
        try:
            return b"".join(chunks)
        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định khi ghép MP3: {e}") from e
