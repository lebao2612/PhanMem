from google.cloud import texttospeech
import google.generativeai as genai
from app.exceptions import HandledException
from config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

gemini_flash = genai.GenerativeModel("gemini-1.5-flash")
gemini_pro = genai.GenerativeModel("gemini-1.5-pro")

_tts_client = texttospeech.TextToSpeechClient.from_service_account_file(
    settings.GOOGLE_TTS_CREDENTIALS_PATH
)


class GeminiClient:
    @staticmethod
    async def _generate_content_async(prompt: str, model_name: str) -> str:
        model = gemini_flash if model_name.lower() == "gemini-1.5-flash" else gemini_pro
        response = await model.generate_content_async(prompt)
        return response.text.strip()

    @staticmethod
    async def generate_suggested_topics(
        keyword: str,
        limit: int = 5,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> list[str]:
        language = language.lower()

        prompt = (
            f"Gợi ý {limit} chủ đề video ngắn đang được quan tâm, ngôn ngữ {language}, "
            f"có liên quan đến từ khóa: \"{keyword}\".\n"
        )
        prompt += "\n".join([
            "- Nội dung phù hợp TikTok, YouTube Shorts",
            "- không tiêu đề, đánh số, chú thích, markdown hay ký tự đặc biệt",
            "- Mỗi dòng là một chủ đề ngắn gọn (tối đa 10 từ)"
        ])

        raw_text = await GeminiClient._generate_content_async(prompt, model_name)
        return GeminiClient._parse_topic_lines(raw_text, limit)

    @staticmethod
    async def generate_trending_topics(
        limit: int = 5,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> list[str]:
        language = language.lower()

        prompt = (
            f"Gợi ý {limit} chủ đề video ngắn đang thịnh hành, ngôn ngữ {language}.\n"
        )
        prompt += "\n".join([
            "- Nội dung phù hợp TikTok, YouTube Shorts",
            "- không tiêu đề, đánh số, chú thích, markdown hay ký tự đặc biệt",
            "- Mỗi dòng là một chủ đề ngắn gọn (tối đa 10 từ)"
        ])

        raw_text = await GeminiClient._generate_content_async(prompt, model_name)
        return GeminiClient._parse_topic_lines(raw_text, limit)

    @staticmethod
    def _parse_topic_lines(raw_text: str, limit: int) -> list[str]:
        valid_topics = []
        for line in raw_text.splitlines():
            cleaned = line.strip("-•. 1234567890").strip()
            if cleaned and len(cleaned.split()) >= 2:
                valid_topics.append(cleaned)
        return valid_topics[:limit]

    @staticmethod
    async def generate_script(
        topic: str,
        language: str = "vi",
        model_name: str = "gemini-1.5-flash"
    ) -> str:
        language = language.lower()

        prompt = "\n".join([
            f"Viết kịch bản video ngắn bằng ngôn ngữ {language}, chủ đề: \"{topic}\". Yêu cầu:",
            "- 3–5 cảnh, mỗi cảnh 1 dòng, định dạng [mô tả ảnh]: [lời thoại/phụ đề sinh động, tự nhiên]",
            "- Không tiêu đề, đánh số, chú tích, markdown hay kí tự đặc biệt"
        ])

        return await GeminiClient._generate_content_async(prompt, model_name)

    @staticmethod
    async def generate_voice(
        script: str,
        gender: str = "female",
        language: str = "vi"
    ) -> bytes:
        try:
            language_code = {
                "vi": "vi-VN",
                "en": "en-US"
            }.get(language.lower(), "vi-VN")

            voice_suffix = {
                "female": "A",
                "male": "B"
            }.get(gender.lower(), "A")

            ssml_gender = {
                "male": texttospeech.SsmlVoiceGender.MALE,
                "female": texttospeech.SsmlVoiceGender.FEMALE
            }.get(gender.lower(), texttospeech.SsmlVoiceGender.NEUTRAL)

            voice_name = f"{language_code}-Standard-{voice_suffix}"

            synthesis_input = texttospeech.SynthesisInput(text=script)
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
                ssml_gender=ssml_gender
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = _tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            return response.audio_content

        except Exception as e:
            raise HandledException(status_code=500, detail=f"TTS generation failed: {e}")
