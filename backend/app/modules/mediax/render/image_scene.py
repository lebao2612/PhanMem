import ffmpeg

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

def get_scale_crop_filter(
    image_path: str,
    pan: str | None,
    output_size: tuple[int, int],
    buffer_ratio: float = 0.1
) -> str:
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

    crop_x = (scale_w - target_w) // 2
    crop_y = (scale_h - target_h) // 2

    return (
        f"scale={scale_w}:{scale_h},"
        f"crop={target_w}:{target_h}:{crop_x}:{crop_y}"
    )