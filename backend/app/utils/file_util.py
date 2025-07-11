import os
import time
import httpx
import tempfile
import filetype
import aiofiles


def create_tempfile(suffix: str = "", prefix: str = "tmp_", dir: str | None = None) -> str:
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    os.close(fd)  # Close file descriptor; caller will write to path
    return path


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


async def download_to_file(url: str, path: str) -> None:
    data = await download_to_bytes(url)
    async with aiofiles.open(path, "wb") as f:
        await f.write(data)


async def download_to_tempfile(url: str) -> str:
    data = await download_to_bytes(url)

    # Dùng filetype để đoán định định dạng
    kind = filetype.guess(data)
    extension = f".{kind.extension}" if kind else ".bin"

    temp_path = create_tempfile(suffix=extension)

    async with aiofiles.open(temp_path, "wb") as f:
        await f.write(data)

    return temp_path


def delete_file(path: str) -> None:
    try:
        if os.path.exists(path):
            time.sleep(0.1) # Tránh File vẫn đang bị giữ bởi process khác
            os.remove(path)
    except PermissionError as e:
        raise PermissionError(f"Không có quyền xoá file: {e}") from e
    except (IOError, OSError) as e:
        raise OSError(f"Lỗi hệ thống khi xoá file: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Lỗi không xác định khi xoá file: {e}") from e
