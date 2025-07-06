import asyncio
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError
from config import settings

class GoogleTTS:
    _client = texttospeech.TextToSpeechClient.from_service_account_file(
        settings.GOOGLE_TTS_CREDENTIALS_PATH
    )
    _audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    _language_code_map = {
        "vi": "vi-VN",
        "en": "en-US"
    }
    _gender_suffix_map = {
        "female": "A",
        "male": "B"
    }
    _ssml_gender_map = {
        "male": texttospeech.SsmlVoiceGender.MALE,
        "female": texttospeech.SsmlVoiceGender.FEMALE
    }

    @staticmethod
    async def generate_voices(
        subtitles: list[str],
        gender: str = "female",
        language: str = "vi"
    ) -> list[bytes]:
        language_code = GoogleTTS._language_code_map.get(language.lower(), "vi-VN")
        voice_suffix = GoogleTTS._gender_suffix_map.get(gender.lower(), "A")
        ssml_gender = GoogleTTS._ssml_gender_map.get(
            gender.lower(),
            texttospeech.SsmlVoiceGender.NEUTRAL
        )

        voice_name = f"{language_code}-Standard-{voice_suffix}"
        try:
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
                ssml_gender=ssml_gender
            )

            async def synthesize(subtitle: str) -> bytes:
                try:
                    synthesis_input = texttospeech.SynthesisInput(text=subtitle)
                    response = await asyncio.to_thread(
                        GoogleTTS._client.synthesize_speech,
                        input=synthesis_input,
                        voice=voice,
                        audio_config=GoogleTTS._audio_config
                    )
                    return response.audio_content
                except GoogleAPIError as e:
                        raise RuntimeError("Không thể kết nối tới Google TTS API.") from e
                
            tasks = [synthesize(subtitle) for subtitle in subtitles if subtitle]
            return await asyncio.gather(*tasks)
    
        except ValueError as e:
            raise ValueError("Dữ liệu đầu vào không hợp lệ.") from e
