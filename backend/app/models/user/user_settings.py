from mongoengine import EmbeddedDocument, StringField

class UserSettings(EmbeddedDocument):
    language = StringField(default="vn")
    theme = StringField(default="dark")
    llm_model = StringField(default="gemini-1.5-flash", choice=["gemini-1.5-flash", "gemini-1.5-pro"])
    tts_model = StringField(default="google-tts", choice=["google-tts"])
    voice_gender = StringField(default="female", choice=["male", "female"])
    tti_model = StringField(default="stable-diffusion", choice=["stable-diffusion"])
