import os

def is_valid_video_file(path: str, valid_exts: list[str] = [".mp4", "mkv"]) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in valid_exts
