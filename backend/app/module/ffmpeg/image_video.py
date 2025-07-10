import os
import ffmpeg

###
def resize_image(image_path: str, width: int, height: int):
    tmp_path = image_path + ".resized.jpg"
    (
        ffmpeg
        .input(image_path)
        .filter("scale", width, height)
        .output(tmp_path)
        .overwrite_output()
        .run(quiet=True)
    )
    os.replace(tmp_path, image_path)

def crop_image(image_path: str, x: int, y: int, width: int, height: int):
    tmp_path = image_path + ".cropped.jpg"
    (
        ffmpeg
        .input(image_path)
        .filter("crop", width, height, x, y)
        .output(tmp_path)
        .overwrite_output()
        .run(quiet=True)
    )
    os.replace(tmp_path, image_path)

###
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