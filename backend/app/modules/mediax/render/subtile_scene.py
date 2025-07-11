import os
import tempfile
import ffmpeg

######
TEMPLATE_ASS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "template.ass")


def burn_subtitle(video_path: str, subtitle: str, duration: float, start_time: float = 0) -> str:
    ass_path = generate_ass_from_template(subtitle, start_time, start_time + duration)
    tmp_output = tempfile.mktemp(suffix=os.path.splitext(video_path)[1] or ".mp4")

    try:
        ass_path_clean = ass_path.replace("\\", "/").replace(":", "\\:")
        (
            ffmpeg
            .input(video_path)
            .output(tmp_output, vf=f"ass='{ass_path_clean}'", vcodec="libx264", acodec="copy")
            .overwrite_output()
            .run(quiet=True)
        )
        os.replace(tmp_output, video_path)
        return video_path
    finally:
        if os.path.exists(ass_path):
            os.remove(ass_path)

def generate_ass_from_template(subtitle: str, start: float, end: float) -> str:
    ass_path = tempfile.mktemp(suffix=".ass")
    with open(TEMPLATE_ASS_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    start_str = format_ass_time(start)
    end_str = format_ass_time(end)
    dialogue_line = f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{subtitle}"

    # Ghép template + dialogue
    if "[Events]" in template:
        header, body = template.split("[Events]", 1)
        result = f"{header}[Events]\n{body.strip()}\n{dialogue_line}\n"
    else:
        result = f"{template.strip()}\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n{dialogue_line}\n"

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(result)

    return ass_path

def format_ass_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{hrs}:{mins:02d}:{secs:02d}.{cs:02d}"
