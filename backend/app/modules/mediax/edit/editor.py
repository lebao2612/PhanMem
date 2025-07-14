import asyncio
import os
import tempfile
import ffmpeg
from app.utils import file_util

async def edit_video(video_url: str, trim=None, theme=None, overlay=None) -> str:
    input_path = await file_util.download_to_tempfile(video_url)
    inputs = []
    filter_lines = []
    vlabel = "[v0]"
    alabel = "[a0]"

    input_stream = ffmpeg.input(input_path)
    inputs.append(input_stream)

    index = 1  # dùng cho các input khác (sticker/audio)

    # === 1. Trim ===
    if trim:
        start = trim["start"]
        end = trim["end"]
        duration = end - start
        input_stream = ffmpeg.input(input_path, ss=start, t=duration)
        inputs[0] = input_stream
        vlabel = "[v0]"
        alabel = "[a0]"

    # === 2. Overlay (sticker + text) ===
    if overlay:
        # Stickers
        for i, s in enumerate(overlay.get("stickers", [])):
            sticker_path = await file_util.download_to_tempfile(s["url"])
            sticker_in = ffmpeg.input(sticker_path, loop=1, t=s["end"] - s["start"])
            inputs.append(sticker_in)
            sticker_id = f"[s{i}]"
            filters = f"[{index}:v]scale=iw*{s['scale']}:ih*{s['scale']}{sticker_id}"
            filter_lines.append(filters)

            out = f"[v{index}]"
            overlay_filter = (
                f"{vlabel}{sticker_id}overlay="
                f"x={s['position'][0]}:y={s['position'][1]}:"
                f"enable='between(t,{s['start']},{s['end']})'{out}"
            )
            filter_lines.append(overlay_filter)
            vlabel = out
            index += 1

        # Texts
        for i, t in enumerate(overlay.get("texts", [])):
            out = f"[v_text{i}]"
            draw = (
                f"{vlabel}drawtext=text='{t['text'].replace("'", '\\\'')}':"
                f"x={t['position'][0]}:y={t['position'][1]}:"
                f"fontcolor={t['color']}:enable='between(t,{t['start']},{t['end']})'{out}"
            )
            filter_lines.append(draw)
            vlabel = out

    # === 3. Theme (music) ===
    if theme and theme.get("music"):
        music_url = theme["music"]["url"]
        volume = theme["music"].get("volume", 1.0)

        music_path = await file_util.download_to_tempfile(music_url)
        music_in = ffmpeg.input(music_path)
        inputs.append(music_in)

        music_label = "[m0]"
        music_filter = f"[{index}:a]volume={volume}{music_label}"
        filter_lines.append(music_filter)

        final_audio = "[final_audio]"
        mix_filter = f"{alabel}{music_label}amix=inputs=2:duration=first:dropout_transition=2{final_audio}"
        filter_lines.append(mix_filter)

        alabel = final_audio
        index += 1

    # === Output ===
    filter_complex = ";".join(filter_lines)
    output_path = tempfile.mktemp(suffix=".mp4")

    stream_args = {
        "vcodec": "libx264",
        "acodec": "aac",
        "pix_fmt": "yuv420p",
        "movflags": "+faststart"
    }

    kwargs = {}
    if filter_complex:
        kwargs["filter_complex"] = filter_complex
        kwargs["map"] = [vlabel, alabel]
    else:
        kwargs["map"] = [inputs[0]["v"], inputs[0]["a"]]

    (
        ffmpeg
        .output(*[i for i in inputs], output_path, **stream_args, **kwargs)
        .overwrite_output()
        .run(quiet=True)
    )

    return output_path


"""
import ffmpeg
from app.utils import file_util
from .filter_builder import build_filter_chain

async def edit_video(video_url: str, trim=None, theme=None, overlay=None) -> str:
    input_path = await file_util.download_to_tempfile(video_url)
    filter_complex, inputs, map_args = await build_filter_chain(input_path, trim, theme, overlay)
    output_path = file_util.create_tempfile(suffix=".mp4")

    (
        ffmpeg
        .output(*inputs, output_path, vf=filter_complex, **map_args)
        .overwrite_output()
        .run(quiet=True)
    )

    return output_path"""