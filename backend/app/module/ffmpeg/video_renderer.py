import os
import asyncio
import httpx
import ffmpeg
import tempfile
from .subtitle_video import burn_subtitle
from .audio_video import get_audio_duration, combine_video_audio
from .image_video import prepare_pan_safe_image



# output_path = folder/file.mp4/ 
async def render_scene(scene: dict, output_path: str, fps=30, output_size: tuple[int, int] = (1080, 1920)):
    # Tạo file tạm cho ảnh và audio
    image_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    audio_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    image_tmp.close()
    audio_tmp.close()
    
    try:
        # 1. Download ảnh và audio
        await asyncio.gather(
            download_file(scene["image"]["url"], image_tmp.name),
            download_file(scene["voice"]["url"], audio_tmp.name)
        )

        # 2. Lấy thời lượng audio làm thời lượng video
        video_duration = get_audio_duration(audio_tmp.name)
        total_frames = int(video_duration * fps)
        # print(video_duration)

        # 3. Hiệu ứng
        effect = scene.get("effect", {})
        zoom_effect = effect.get("zoom")
        pan_effect = effect.get("pan")
        assert not (zoom_effect and pan_effect), "Cannot specify both zoom and pan effects at the same time"
        effect_duration = effect.get("duration", video_duration)
        effect_frames = int(min(effect_duration, video_duration) * fps)

        prepare_pan_safe_image(
            image_path=image_tmp.name,
            pan=pan_effect,
            output_size=output_size,
            buffer_ratio=0.1
        )

        (
            ffmpeg
            .input(image_tmp.name, loop=1, framerate=fps, t=video_duration)
            .filter("zoompan",
                    z=get_zoom_expr(zoom_effect, effect_frames),
                    x=get_pan_x_expr(pan_effect, effect_frames),
                    y=get_pan_y_expr(pan_effect, effect_frames),
                    d=total_frames,
                    s=f"{output_size[0]}x{output_size[1]}")
            .output(output_path,
                    vcodec="libx264",
                    pix_fmt="yuv420p",
                    r=fps,
                    t=video_duration,
                    an=None)
            .overwrite_output()
            .run(quiet=True)
        )

        # 7. Burn phụ đề
        # burn_subtitle(
        #     video_path=output_path,
        #     subtitle=scene["subtitle"],
        #     start_time=0.0,
        #     duration=video_duration
        # )

        # 8. Ghép audio
        combine_video_audio(
            video_path=output_path,
            audio_path=audio_tmp.name
        )
    finally:
        if os.path.exists(image_tmp.name):
            os.remove(image_tmp.name)
        if os.path.exists(audio_tmp.name):
            os.remove(audio_tmp.name)


####
def concat_videos(video_paths: list[str], output_path: str):
    """
    Ghép nhiều video lại thành 1 video bằng concat demuxer (copy codec).
    """
    list_path = tempfile.mktemp(suffix=".txt")
    try:
        with open(list_path, "w", encoding="utf-8") as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        (
            ffmpeg
            .input(list_path, format="concat", safe=0)
            .output(output_path, c="copy")
            .overwrite_output()
            .run(quiet=True)
        )
    finally:
        if os.path.exists(list_path):
            os.remove(list_path)


async def render_video(scenes: list[dict], output_path: str, suffix=".mkv"):
    try:
        # 1. Tạo file tạm cho mỗi scene
        temp_video_paths = [
            tempfile.NamedTemporaryFile(delete=False, suffix=suffix).name
            for _ in scenes
        ]
        

        # 2. Render song song các scene
        await asyncio.gather(*[
            render_scene(scene, temp_path)
            for scene, temp_path in zip(scenes, temp_video_paths)
        ])

        # 3. Gộp lại thành 1 video cuối cùng
        concat_videos(temp_video_paths, output_path)
    except Exception as e:
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
        raise RuntimeError(f"Có lỗi xảy ra khi render video: {e}") from e
    finally:
        for path in temp_video_paths:
            if os.path.exists(path):
                os.remove(path)







async def download_file(url: str, output_path: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)

def get_zoom_expr(zoom: str | None, effect_frames: int) -> str:
    if not zoom:
        return "zoom"
    return {
        "in": f"if(lte(on,{effect_frames}),zoom+0.001,zoom)",
        "out": f"if(lte(on,{effect_frames}),zoom-0.001,zoom)"
    }.get(zoom, "zoom")

def get_pan_x_expr(pan: str | None, effect_frames: int) -> str:
    if pan not in ("left", "right"):
        return "x"
    return {
        "left": f"if(lte(on,{effect_frames}),x-1.1,x)",
        "right": f"if(lte(on,{effect_frames}),x+1.1,x)"
    }[pan]

def get_pan_y_expr(pan: str | None, effect_frames: int) -> str:
    if pan not in ("up", "down"):
        return "y"
    return {
        "up": f"if(lte(on,{effect_frames}),y-1.1,y)",
        "down": f"if(lte(on,{effect_frames}),y+1.1,y)"
    }[pan]
