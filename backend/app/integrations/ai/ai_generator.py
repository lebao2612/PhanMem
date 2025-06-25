import os
import uuid
from typing import List
from app.models import Video

from google.cloud import texttospeech
from fastapi import HTTPException
import aiofiles
import cloudinary
import cloudinary.uploader

class AIGenerator:

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    @staticmethod
    async def generate_topic_suggestions(keyword: str, limit: int) -> List[str]:
        if not keyword:
            # Mock general topics
            return [f"Suggestion trend {i}" for i in range(1, limit + 1)]
        
        # Mock topic suggestions based on query
        return [f"{keyword} trend {i}" for i in range(1, limit + 1)]

    @staticmethod
    async def generate_trending_topics(limit: int) -> List[str]:
        # Mock trending topics
        return ["Tech 2025", "AI Tutorial", "Short Video Trends"]

    @staticmethod
    async def generate_script(topic: str) -> str:
        # Mock script
        return f"Đây là đoạn script mô phỏng từ chủ đề: '{topic}'. Nội dung chi tiết sẽ do AI tạo ra sau."

    @staticmethod
    async def generate_voice(full_script: str) -> str:
        filename = f"tts_{uuid.uuid4().hex}.mp3"

        try:
            # Tạo client Google TTS
            client = texttospeech.TextToSpeechClient.from_service_account_file("tts_secret.json")

            # Tạo input cho TTS
            synthesis_input = texttospeech.SynthesisInput(text=full_script)

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

            # Ghi ra file tạm
            async with aiofiles.open(filename, "wb") as out:
                await out.write(response.audio_content)

            # Upload lên Cloudinary
            uploaded = cloudinary.uploader.upload(
                filename,
                resource_type="video",  # Cloudinary xem mp3 là video
                folder="tts-audio"
            )

            # Trả về URL
            return uploaded["secure_url"]

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")

        finally:
            # Đảm bảo xóa file tạm nếu tồn tại
            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except Exception as remove_err:
                    print(f"Warning: Failed to delete temp file {filename}: {remove_err}")


    @staticmethod
    async def generate_background_image(topic: str) -> str:
        # TODO

        # Mock background image URL
        return "https://res.cloudinary.com/df8meqyyc/image/upload/v1750280031/tech2025_hgsl68.jpg"

    @staticmethod
    async def generate_video(video: Video) -> str:
        # TODO

        # Mock video URL
        return "https://res.cloudinary.com/df8meqyyc/video/upload/v1750280402/text-to-video_rmp4vx.mp4"