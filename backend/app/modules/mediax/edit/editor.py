import os
import ffmpeg
import asyncio
from app.utils import file_util
from app.modules.mediax import ops



async def edit_video(video_url: str, trim=None, theme=None, overlay=None) -> str:
    raise NotImplementedError("Not implement")
    # # 1. Download video đầu vào
    # input_path = await file_util.download_to_tempfile(video_url)

    # # 2. Tạo filter_complex (dây chuyền filter) cho ffmpeg
    # filter_complex, input_streams, extra_args = await build_filter_chain(
    #     input_path, trim=trim, theme=theme, overlay=overlay
    # )

    # # 3. Gọi ffmpeg một lần duy nhất
    # output_path = file_util.create_tempfile(suffix=".mp4")

    # (
    #     ffmpeg
    #     .concat(*input_streams, v=1, a=1)
    #     .output(output_path, **extra_args, vf=filter_complex)
    #     .overwrite_output()
    #     .run(quiet=True)
    # )

    # return output_path