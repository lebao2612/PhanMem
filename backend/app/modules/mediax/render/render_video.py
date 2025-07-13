import asyncio
from app.modules.mediax import ops
from app.utils import file_util
from .render_scene import render_scene

async def render_video(scenes: list[dict], suffix=".mp4") -> str:
    try:
        video_path = file_util.create_tempfile(suffix=suffix)

        # 1. Tạo file tạm cho mỗi scene
        temp_video_paths = [
            file_util.create_tempfile(suffix=suffix)
            for _ in scenes
        ]  
        # 2. Render song song các scene
        await asyncio.gather(*[
            render_scene(scene, temp_path)
            for scene, temp_path in zip(scenes, temp_video_paths)
        ])
        # 3. Gộp lại thành 1 video cuối cùng
        ops.video.concat_videos(temp_video_paths, video_path)

        return video_path
    except Exception as e:
        raise RuntimeError(str(e)) from e
    finally:
        for path in temp_video_paths:
            file_util.delete_file(path=path)
