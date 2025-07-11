import os
import tempfile
import ffmpeg

def is_valid_video_file(path: str, valid_exts: list[str] = [".mp4", "mkv"]) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in valid_exts

def concat_videos(video_paths: list[str], output_path: str):
    """
    Ghép nhiều video lại thành 1 video bằng concat demuxer (copy codec).
    """
    list_path = tempfile.mktemp(suffix=".txt")
    try:
        with open(list_path, "w", encoding="utf-8") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        (
            ffmpeg
            .input(list_path, format="concat", safe=0)
            .output(output_path, c="copy")
            .overwrite_output()
            .run(quiet=True)
        )
    finally:
        if os.path.exists(list_path):
            os.remove(list_path)
