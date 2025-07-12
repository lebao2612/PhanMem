import tempfile
import os

TEMPLATE_ASS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "template.ass")

def format_ass_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{hrs}:{mins:02d}:{secs:02d}.{cs:02d}"

def auto_wrap_text(text: str, max_chars_per_line: int = 33) -> str:
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # Thử thêm từ vào dòng hiện tại
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            # Xuống dòng nếu vượt quá giới hạn
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return r"\N".join(lines)


def generate_ass_from_template(subtitle: str, start: float, end: float) -> str:
    ass_path = tempfile.mktemp(suffix=".ass")

    # Đọc template .ass sẵn có
    with open(TEMPLATE_ASS_PATH, "r", encoding="utf-8") as f:
        template = f.read().strip()

    # Tự động xuống dòng nếu quá dài
    wrapped_text = auto_wrap_text(subtitle, max_chars_per_line=33)

    # Chuyển đổi thời gian sang định dạng ASS
    start_str = format_ass_time(start)
    end_str = format_ass_time(end)

    # Tạo dòng phụ đề
    dialogue_line = f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{wrapped_text}"

    # Ghép nội dung .ass hoàn chỉnh
    if "[Events]" in template:
        header, body = template.split("[Events]", 1)
        content = f"{header.strip()}\n[Events]\n{body.strip()}\n{dialogue_line}\n"
    else:
        content = (
            f"{template}\n[Events]\n"
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            f"{dialogue_line}\n"
        )

    # Ghi ra file tạm thời
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(content)

    return ass_path
