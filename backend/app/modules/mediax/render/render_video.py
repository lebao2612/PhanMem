import os
import asyncio
import ffmpeg
from app.utils import file_util
from app.modules.mediax import ops
from .effect_scene import get_pan_x_expr, get_pan_y_expr, get_zoom_expr
from .subtile_scene import generate_ass_from_template
from .image_scene import get_scale_crop_filter

async def render_scene(scene: dict, output_path: str, fps=30, output_size: tuple[int, int] = (1080, 1920)):
    try:
        # 1. Download ảnh và audio song song
        image_path, audio_path = await asyncio.gather(
            file_util.download_to_tempfile(scene["image"]["url"]),
            file_util.download_to_tempfile(scene["voice"]["url"])
        )

        # 2. Lấy thời lượng video từ audio
        video_duration = ops.audio.get_audio_duration(audio_path)
        total_frames = int(video_duration * fps)

        # 3. Hiệu ứng zoom/pan
        effect = scene.get("effect", {})
        zoom_effect = effect.get("zoom")
        pan_effect = effect.get("pan")

        if not zoom_effect and not pan_effect:
            zoom_effect = "in"
        elif zoom_effect:
            pan_effect = None

        effect_frames = video_duration * fps

        # 4. Subtitle: generate file .ass
        ass_path = generate_ass_from_template(
            subtitle=scene["subtitle"],
            start=0.0,
            end=video_duration
        )
        
        ass_path_clean = ass_path.replace("\\", "/").replace(":", "\\:")

        # 5. Build filter chain
        pre_zoom_filter = get_scale_crop_filter(image_path, pan_effect, output_size)
        zoompan_filter = (
            f"zoompan="
            f"z='{get_zoom_expr(zoom_effect, effect_frames)}':"
            f"x='{get_pan_x_expr(pan_effect, effect_frames)}':"
            f"y='{get_pan_y_expr(pan_effect, effect_frames)}':"
            f"d={total_frames}:"
            f"s={output_size[0]}x{output_size[1]}"
        )
        vf_chain = f"{pre_zoom_filter},{zoompan_filter},ass='{ass_path_clean}'"

        # 6. Gọi ffmpeg
        input_image = ffmpeg.input(image_path, loop=1, framerate=fps, t=video_duration)
        input_audio = ffmpeg.input(audio_path)

        (
            ffmpeg
            .output(
                input_image.video, input_audio.audio,
                output_path,
                vf=vf_chain,
                vcodec="libx264",
                acodec="aac",
                pix_fmt="yuv420p",
                r=fps,
                t=video_duration
            )
            .overwrite_output()
            .run(quiet=True)
        )

    finally:
        file_util.delete_file(audio_path)
        file_util.delete_file(image_path)
        file_util.delete_file(ass_path)


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
