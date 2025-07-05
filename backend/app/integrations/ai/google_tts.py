from google.cloud import texttospeech
from app.exceptions import HandledException
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
    async def generate_voice(
        subtitles: list[str],
        gender: str = "female",
        language: str = "vi"
    ) -> list[bytes]:
        try:
            lang_key = language.lower()
            gender_key = gender.lower()

            language_code = GoogleTTS._language_code_map.get(lang_key, "vi-VN")
            voice_suffix = GoogleTTS._gender_suffix_map.get(gender_key, "A")
            ssml_gender = GoogleTTS._ssml_gender_map.get(
                gender_key,
                texttospeech.SsmlVoiceGender.NEUTRAL
            )

            voice_name = f"{language_code}-Standard-{voice_suffix}"

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
                ssml_gender=ssml_gender
            )

            audio_chunks = []

            for subtitle in subtitles:
                if not subtitle:
                    continue

                synthesis_input = texttospeech.SynthesisInput(text=subtitle)
                response = GoogleTTS._client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=GoogleTTS._audio_config
                )
                audio_chunks.append(response.audio_content)

            return audio_chunks

        except Exception as e:
            raise HandledException(status_code=500, detail=f"TTS generation failed: {e}")
