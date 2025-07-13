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

    return output_path