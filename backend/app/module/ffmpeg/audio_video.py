import os
import ffmpeg

def combine_video_audio(video_path: str, audio_path: str):
    """
    Ghép audio vào video (sử dụng file tạm), giữ nguyên định dạng .mp4.
    """
    base, ext = os.path.splitext(video_path)
    tmp_path = f"{base}.tmp{ext}"  # ex: scene_1.tmp.mp4

    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)

    (
        ffmpeg
        .output(input_video, input_audio, tmp_path, vcodec="copy", acodec="aac", strict="experimental")
        .overwrite_output()
        .run(quiet=True)
    )

    os.replace(tmp_path, video_path)


def get_audio_duration(audio_path: str) -> float:
    probe = ffmpeg.probe(audio_path)
    return float(probe["format"]["duration"])


def cut_audio(audio_path: str, start: float, duration: float, format: str = "mp3"):
    (
        ffmpeg
        .input(audio_path, ss=start, t=duration)
        .output(audio_path, format=format)
        .overwrite_output()
        .run(quiet=True)
    )

def change_volume(audio_path: str, volume: float, format: str = "mp3"):
    (
        ffmpeg
        .input(audio_path)
        .output(audio_path, af=f"volume={volume}", format=format)
        .overwrite_output()
        .run(quiet=True)
    )