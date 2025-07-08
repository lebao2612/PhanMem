import asyncio
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError


class GoogleTTSClient:
    def __init__(self, credentials_path: str):
        try:
            self._client = texttospeech.TextToSpeechClient.from_service_account_file(
                credentials_path
            )
            self._audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
        except Exception as e:
            raise RuntimeError("Lỗi khi khởi tạo Google TTS client hoặc audio config.") from e

        self._language_code_map = {
            "vi": "vi-VN",
            "en": "en-US"
        }
        self._gender_suffix_map = {
            "female": "A",
            "male": "B"
        }
        self._ssml_gender_map = {
            "male": texttospeech.SsmlVoiceGender.MALE,
            "female": texttospeech.SsmlVoiceGender.FEMALE
        }

    async def generate_voices(
        self,
        subtitles: list[str],
        voice_gender: str = "female",
        language: str = "vi"
    ) -> list[bytes]:
        language_code = self._language_code_map.get(language.lower(), "vi-VN")
        voice_suffix = self._gender_suffix_map.get(voice_gender.lower(), "A")
        ssml_gender = self._ssml_gender_map.get(
            voice_gender.lower(),
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
                        self._client.synthesize_speech,
                        input=synthesis_input,
                        voice=voice,
                        audio_config=self._audio_config
                    )
                    return response.audio_content
                except GoogleAPIError as e:
                    raise RuntimeError("Không thể kết nối tới Google TTS API.") from e

            tasks = [synthesize(sub) for sub in subtitles if sub]
            return await asyncio.gather(*tasks)

        except ValueError as e:
            raise ValueError("Dữ liệu đầu vào không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError(f"Có lỗi xảy ra khi gen voice: {e}") from e
