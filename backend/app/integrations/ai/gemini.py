import re
import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self._gemini_flash = genai.GenerativeModel("gemini-1.5-flash")
        self._gemini_pro = genai.GenerativeModel("gemini-1.5-pro")
        self._models = {
            "gemini-1.5-flash": self._gemini_flash,
            "gemini-1.5-pro": self._gemini_pro
        }

    async def generate_suggested_topics(
        self,
        keyword: str,
        limit: int = 5,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> list[str]:
        prompt = (
            f"Gợi ý [{limit}] chủ đề video ngắn đang được quan tâm, ngôn ngữ [{language}], "
            f"có liên quan đến từ khóa: [{keyword}].\n"
        ) + "\n".join([
            "- Nội dung phù hợp TikTok, YouTube Shorts",
            "- không tiêu đề, đánh đầu dòng, chú thích, markdown hay ký tự đặc biệt",
            "- Mỗi dòng là một chủ đề ngắn gọn (tối đa 10 từ)"
        ])

        raw_text = await self._generate_content_async(prompt, model_name)
        return [line.strip() for line in raw_text.splitlines() if line.strip()][:limit]

    async def generate_trending_topics(
        self,
        limit: int = 5,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> list[str]:
        prompt = (
            f"Gợi ý {limit} chủ đề video ngắn đang thịnh hành, ngôn ngữ [{language}].\n"
        ) + "\n".join([
            "- Nội dung phù hợp TikTok, YouTube Shorts",
            "- không tiêu đề, đánh đầu dòng, chú thích, markdown hay ký tự đặc biệt",
            "- Mỗi dòng là một chủ đề ngắn gọn (tối đa 20 từ)"
        ])

        raw_text = await self._generate_content_async(prompt, model_name)
        return [line.strip() for line in raw_text.splitlines() if line.strip()][:limit]

    async def generate_script(
        self,
        topic: str,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash",
        scene_count: int = 5
    ) -> list[dict]:
        prompt = "\n".join([
            f"Viết kịch bản video ngắn bằng ngôn ngữ [{language}], chủ đề: [{topic}]. Yêu cầu:",
             "- Không tiêu đề, đánh đầu dòng, chú thích, markdown hay kí tự đặc biệt",
            f"- Gồm [{scene_count}] cảnh, các cảnh phải có liên kết với nhau",
             "- mỗi cảnh 1 dòng duy nhất, định dạng:",
             "mô tả ảnh ## lời thoại/phụ đề sinh động, tự nhiên",
        ])

        raw_text = await self._generate_content_async(prompt, model_name)
        scene_count = []
        for line in raw_text.splitlines():
            if line.strip():
                parts = line.split("##")
                if len(parts) == 2:
                    scene_count.append({
                        "label": parts[0].strip(),
                        "subtitle": parts[1].strip()
                    })
        return scene_count

    async def _generate_content_async(self, prompt: str, model_name: str) -> str:
        model = self._models.get(model_name, self._gemini_flash)

        try:
            response = await model.generate_content_async(prompt)
            raw_text = response.text.strip()

            # Làm sạch dữ liệu đầu ra
            cleaned_text = re.sub(r"(?m)^[\s\-–•\d\.\)\(]+", "", raw_text)
            cleaned_text = "\n".join(
                line for line in cleaned_text.splitlines() if line.strip()
            )
            return cleaned_text

        except Exception as e:
            raise RuntimeError(f"Lỗi khi gọi Gemini API: {e}") from e
