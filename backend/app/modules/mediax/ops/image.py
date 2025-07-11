import os
import ffmpeg

def is_valid_image_file(path: str, valid_exts: list[str] = [".jpg", ".jpeg", ".png"]) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in valid_exts


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
