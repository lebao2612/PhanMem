import ffmpeg
from app.utils import file_util

async def build_theme_filters(audio_label: str, theme: dict | None):
    if not theme or not theme.get("music"):
        return [], [f"{audio_label}anull[aout]"]

    music = theme["music"]
    music_path = await file_util.download_to_tempfile(music["url"])
    music_input = ffmpeg.input(music_path)
    inputs = [music_input]

    vol = music.get("volume", 1.0)
    filters = []

    if vol != 1.0:
        filters.append(f"[1:a]volume={vol}[music_vol]")
        filters.append(f"{audio_label}[music_vol]amix=inputs=2:duration=shortest[aout]")
    else:
        filters.append(f"{audio_label}[1:a]amix=inputs=2:duration=shortest[aout]")

    return inputs, filters
