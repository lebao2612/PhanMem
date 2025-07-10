import os
import ffmpeg
import tempfile

def burn_subtitle(video_path: str, subtitle: str, duration: float, start_time: float = 0) -> str:
    srt_path = tempfile.mktemp(suffix=".srt")
    tmp_output = tempfile.mktemp(suffix=os.path.splitext(video_path)[1] or ".mp4")

    try:
        start = format_srt_time(start_time)
        end = format_srt_time(start_time + duration)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(f"1\n{start} --> {end}\n{subtitle}\n")

        srt_path_clean = srt_path.replace("\\", "/").replace(":", "\\:")

        (
            ffmpeg
            .input(video_path)
            .filter("subtitles", srt_path_clean)
            .output(tmp_output,filter_complex=f'subtitles={srt_path_clean}', vcodec="libx264", acodec="copy")
            .overwrite_output()
            .run()
        )

        os.replace(tmp_output, video_path)
        return video_path
    finally:
        if os.path.exists(srt_path):
            os.remove(srt_path)

def format_srt_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"
