import ffmpeg

def build_video_input(input_path: str, trim: dict | None):
    trim_args = {"ss": trim["start"], "to": trim["end"]} if trim else {}
    input_stream = ffmpeg.input(input_path, **trim_args)
    return input_stream, "[0:v]", "[0:a]"
