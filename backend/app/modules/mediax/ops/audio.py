import ffmpeg
import os

def is_valid_image_file(path: str, valid_exts: list[str] = [".jpg", ".jpeg", ".png"]) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in valid_exts


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