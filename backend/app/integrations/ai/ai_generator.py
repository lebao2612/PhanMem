from typing import List
from google.cloud import texttospeech
from config import settings
from app.models import Video
from app.exceptions import HandledException
import requests


class AIGenerator:
    @staticmethod
    async def generate_script(topic: str) -> str:
        prompt = f"Viết kịch bản ~100 chữ cho video AI chủ đề \"{topic}\". Chỉ trả về văn bản thuần."
        return AIGenerator.ask_llm(prompt)

    @staticmethod
    async def generate_topic_suggestions(keyword: str, limit: int) -> List[str]:
        if not keyword:
            return await AIGenerator.generate_trending_topics(limit)
        prompt = f"Gợi ý {limit} chủ đề video AI liên quan đến \"{keyword}\". Mỗi dòng là 1 chủ đề."
        raw = AIGenerator.ask_llm(prompt)
        return [line.strip("-•. ") for line in raw.splitlines() if line.strip()]

    @staticmethod
    async def generate_trending_topics(limit: int) -> List[str]:
        prompt = f"Gợi ý {limit} chủ đề video AI đang thịnh hành. Mỗi dòng là 1 chủ đề."
        raw = AIGenerator.ask_llm(prompt)
        return [line.strip("-•. ") for line in raw.splitlines() if line.strip()]

    @staticmethod
    async def generate_voice(script: str) -> bytes:
        try:
            # Tạo client Google TTS
            client = texttospeech.TextToSpeechClient.from_service_account_file(settings.GOOGLE_TTS_SERVICE_ACCOUNT_PATH)

            # Tạo input cho TTS
            synthesis_input = texttospeech.SynthesisInput(text=script)

            # Cấu hình giọng nói
            voice = texttospeech.VoiceSelectionParams(
                language_code="vi-VN",
                name="vi-VN-Standard-A",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            # Cấu hình định dạng âm thanh
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Gọi TTS API
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            return response.audio_content

        except Exception as e:
            raise HandledException(status_code=500, detail=f"TTS generation failed: {e}")

    @staticmethod
    async def generate_images(topic: str) -> str:
        # TODO

        # Mock background image URL
        return "https://res.cloudinary.com/df8meqyyc/image/upload/v1750280031/tech2025_hgsl68.jpg"

    @staticmethod
    async def generate_video(video: Video) -> bytes:
        # TODO

        # Mock video URL
        return None
    
    @staticmethod
    def ask_llm(prompt: str) -> str:
        url = settings.LLM_API_URL
        headers = {
            "Authorization": f"Bearer {settings.LLM_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": settings.LLM_API_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Bạn là trợ lý viết nội dung video ngắn. Trả text, không tiêu đề, không giải thích."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise Exception(f"Lỗi gọi LLM: {e}")