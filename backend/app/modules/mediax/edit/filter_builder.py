from .filter_parts.video_input import build_video_input
from .filter_parts.overlay import build_overlay_filters
from .filter_parts.theme import build_theme_filters


async def build_filter_chain(input_path: str, trim=None, theme=None, overlay=None):
    inputs = []
    filter_lines = []

    # Video/audio input (trim)
    video_input, video_label, audio_label = build_video_input(input_path, trim)
    inputs.append(video_input)

    # Overlay filters
    video_label, overlay_inputs, overlay_lines = await build_overlay_filters(video_label, overlay)
    inputs.extend(overlay_inputs)
    filter_lines.extend(overlay_lines)

    # Theme/music filters
    theme_inputs, theme_lines = await build_theme_filters(audio_label, theme)
    inputs.extend(theme_inputs)
    filter_lines.extend(theme_lines)

    filter_complex = ";".join(filter_lines)

    return filter_complex, inputs, {
        "map": video_label,
        "map": "[aout]",
        "vcodec": "libx264",
        "acodec": "aac",
        "pix_fmt": "yuv420p",
        "shortest": None
    }
