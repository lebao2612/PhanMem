import os
import asyncio
import httpx
import ffmpeg
import tempfile
from app.utils import file_util
from .audio import get_audio_duration, is_valid_image_file
from .image import crop_image, resize_image, is_valid_image_file

# output_path = folder/file.mp4/ 
async def render_scene(scene: dict, output_path: str, fps=30, output_size: tuple[int, int] = (1080, 1920)):
    try:
        # 1. Download ảnh và audio
        image_path, audio_path = await asyncio.gather(
            file_util.download_to_tempfile(scene["image"]["url"]),
            file_util.download_to_tempfile(scene["voice"]["url"])
        )

        # 2. Lấy thời lượng audio làm thời lượng video
        video_duration = get_audio_duration(audio_path)
        total_frames = int(video_duration * fps)
        # print(video_duration)

        # 3. Hiệu ứng
        effect = scene.get("effect", {})
        zoom_effect = effect.get("zoom")
        pan_effect = effect.get("pan")
        # assert not (zoom_effect and pan_effect), "Cannot specify both zoom and pan effects at the same time"
        if not zoom_effect and not pan_effect:
            zoom_effect = "in"
        elif zoom_effect:
            pan_effect = None
        
        effect_duration = effect.get("duration", video_duration)
        effect_frames = int(min(effect_duration, video_duration) * fps)

        prepare_pan_safe_image(
            image_path=image_path,
            pan=pan_effect,
            output_size=output_size,
            buffer_ratio=0.1
        )
        (
            ffmpeg
            .input(image_path, loop=1, framerate=fps, t=video_duration)
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
        burn_subtitle(
            video_path=output_path,
            subtitle=scene["subtitle"],
            start_time=0.0,
            duration=video_duration
        )

        # 8. Ghép audio
        combine_video_audio(
            video_path=output_path,
            audio_path=audio_path
        )
    finally:
        file_util.delete_file(audio_path)
        file_util.delete_file(image_path)


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



########
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

######
def combine_video_audio(video_path: str, audio_path: str):
    """
    Ghép audio vào video (sử dụng file tạm), giữ nguyên định dạng .mp4.
    """
    base, ext = os.path.splitext(video_path)
    tmp_path = f"{base}.tmp{ext}"  # ex: scene_1.tmp.mp4

    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)

    (
        ffmpeg
        .output(input_video, input_audio, tmp_path, vcodec="copy", acodec="aac", strict="experimental")
        .overwrite_output()
        .run(quiet=True)
    )

    os.replace(tmp_path, video_path)

######
def compute_buffered_dimensions(
    pan: str | None,
    output_size: tuple[int, int],
    buffer_ratio: float
) -> tuple[int, int]:
    target_w, target_h = output_size

    if pan in ("left", "right"):
        target_w = int(target_w * (1 + buffer_ratio))
    elif pan in ("up", "down"):
        target_h = int(target_h * (1 + buffer_ratio))

    return target_w, target_h

def prepare_pan_safe_image(
    image_path: str,
    pan: str | None = None,
    output_size: tuple[int, int] = (1080, 1920),
    buffer_ratio: float = 0.1
):
    target_w, target_h = output_size

    extra_w, extra_h = compute_buffered_dimensions(pan, output_size, buffer_ratio)

    probe = ffmpeg.probe(image_path)["streams"][0]
    iw = int(probe["width"])
    ih = int(probe["height"])
    aspect = iw / ih

    if aspect > (extra_w / extra_h):
        scale_h = extra_h
        scale_w = int(scale_h * aspect)
    else:
        scale_w = extra_w
        scale_h = int(scale_w / aspect)

    resize_image(image_path, scale_w, scale_h)

    crop_x = (scale_w - target_w) // 2
    crop_y = (scale_h - target_h) // 2
    crop_image(image_path, crop_x, crop_y, target_w, target_h)

######
TEMPLATE_ASS_PATH = "assets/template/template.ass"

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
