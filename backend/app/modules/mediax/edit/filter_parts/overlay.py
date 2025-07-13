import ffmpeg
from app.utils import file_util

async def build_overlay_filters(input_label: str, overlay: dict | None):
    if not overlay:
        return input_label, [], []

    inputs = []
    filters = []
    current_label = input_label

    # Stickers
    for i, s in enumerate(overlay.get("stickers", [])):
        sticker_path = await file_util.download_to_tempfile(s["url"])
        s_input = ffmpeg.input(sticker_path, loop=1, t=s["end"] - s["start"])
        inputs.append(s_input)

        scaled = f"[ss{i}]"
        filters.append(f"[{len(inputs)}:v]scale=iw*{s['scale']}:ih*{s['scale']}{scaled}")

        out = f"[v{i+1}]"
        filters.append(
            f"{current_label}{scaled}overlay="
            f"x={s['position'][0]}:y={s['position'][1]}:"
            f"enable='between(t,{s['start']},{s['end']})'{out}"
        )
        current_label = out

    # Texts
    for i, t in enumerate(overlay.get("texts", [])):
        txt = t["text"].replace("'", "\\'")
        out = f"[v_text{i}]"
        filters.append(
            f"{current_label}drawtext=text='{txt}':x={t['position'][0]}:y={t['position'][1]}:"
            f"fontcolor={t['color']}:enable='between(t,{t['start']},{t['end']})'{out}"
        )
        current_label = out

    return current_label, inputs, filters
