import re
import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

class GeminiClient:
    _gemini_flash = genai.GenerativeModel("gemini-1.5-flash")
    _gemini_pro = genai.GenerativeModel("gemini-1.5-pro")

    _model = {
        "gemini_flash": _gemini_flash,
        "gemini_pro" : _gemini_pro
    }

    @staticmethod
    async def _generate_content_async(prompt: str, model_name: str) -> str:
        model = GeminiClient._model.get(model_name, GeminiClient._gemini_flash)
        # model = gemini_pro if model_name.lower() != "gemini-1.5-flash" else gemini_flash

        response = await model.generate_content_async(prompt)
        raw_text = response.text.strip()
        
        # Loại bỏ ký tự đặc biệt, số, dấu đầu dòng từ đầu mỗi dòng
        cleaned_text = re.sub(r"(?m)^[\s\-–•\d\.\)\(]+", "", raw_text)
        # Loại bỏ dòng trống
        cleaned_text = "\n".join(line for line in cleaned_text.splitlines() if line.strip())
        return cleaned_text

    @staticmethod
    async def generate_suggested_topics(
        keyword: str,
        limit: int = 5,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> list[str]:
        prompt = (
            f"Gợi ý {limit} chủ đề video ngắn đang được quan tâm, ngôn ngữ {language}, "
            f"có liên quan đến từ khóa: \"{keyword}\".\n"
        )
        prompt += "\n".join([
            "- Nội dung phù hợp TikTok, YouTube Shorts",
            "- không tiêu đề, đánh đầu dòng, chú thích, markdown hay ký tự đặc biệt",
            "- Mỗi dòng là một chủ đề ngắn gọn (tối đa 10 từ)"
        ])

        raw_text = await GeminiClient._generate_content_async(prompt, model_name)
        return [line.strip() for line in raw_text.splitlines() if line.strip()][:limit]

    @staticmethod
    async def generate_trending_topics(
        limit: int = 5,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> list[str]:
        prompt = (
            f"Gợi ý {limit} chủ đề video ngắn đang thịnh hành, ngôn ngữ {language}.\n"
        )
        prompt += "\n".join([
            "- Nội dung phù hợp TikTok, YouTube Shorts",
            "- không tiêu đề, đánh đầu dòng, chú thích, markdown hay ký tự đặc biệt",
            "- Mỗi dòng là một chủ đề ngắn gọn (tối đa 10 từ)"
        ])

        raw_text = await GeminiClient._generate_content_async(prompt, model_name)
        return [line.strip() for line in raw_text.splitlines() if line.strip()][:limit]

    @staticmethod
    async def generate_script(
        topic: str,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> list[dict]:
        prompt = "\n".join([
            f"Viết kịch bản video ngắn bằng ngôn ngữ {language}, chủ đề: \"{topic}\". Yêu cầu:",
            "Không tiêu đề, đánh đầu dòng, chú tích, markdown hay kí tự đặc biệt",
            "Gồm 3-5 cảnh, mỗi cảnh 1 dòng, định dạng:",
            "mô tả ảnh ## lời thoại/phụ đề sinh động, tự nhiên",
        ])

        raw_text = await GeminiClient._generate_content_async(prompt, model_name)
        scenes = []
        for line in raw_text.splitlines():
            if line.strip():
                parts = line.split("##")
                if len(parts) == 2:
                    scenes.append({"label": parts[0].strip(), "subtitle": parts[1].strip()})
        return scenes
