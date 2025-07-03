from google.cloud import texttospeech
from app.exceptions import HandledException
from config import settings
_tts_client = texttospeech.TextToSpeechClient.from_service_account_file(
    settings.GOOGLE_TTS_CREDENTIALS_PATH
)

class GoogleTTS:
    @staticmethod
    async def generate_voice(
        subtitles: list[str],
        gender: str = "female",
        language: str = "vi"
    ) -> list[bytes]:
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

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
                ssml_gender=ssml_gender
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            audio_chunks = []

            for subtitle in subtitles:
                if not subtitle:
                    continue

                synthesis_input = texttospeech.SynthesisInput(text=subtitle)
                response = _tts_client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config
                )
                audio_chunks.append(response.audio_content)

            return audio_chunks

        except Exception as e:
            raise HandledException(status_code=500, detail=f"TTS generation failed: {e}")
