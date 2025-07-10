from mongoengine import EmbeddedDocument, StringField, ListField

class UserSettings(EmbeddedDocument):
    language = StringField(default="vi", choices=["vi", "en"])
    theme = StringField(default="dark", choices=["dark", "light"])
    llm_model = StringField(default="gemini-1.5-flash", choices=["gemini-1.5-flash", "gemini-1.5-pro"])
    tts_model = StringField(default="google-tts", choices=["google-tts"])
    voice_gender = StringField(default="female", choices=["male", "female"])
    tti_model = StringField(default="stable-diffusion", choices=["stable-diffusion"])
    personality = ListField(StringField())

"""
hoạt ngôn
hóm hỉnh
thẳng thắn
khích lệ
phong cách gen z
hoài nghi
truyền thống
tư tưởng tân tiến
thơ mộng
tùy chỉnh
"""