# === OAuth 2.0 endpoints (fixed) ===
GOOGLE_OAUTH_ENDPOINTS = {
    "AUTH_URI": "https://accounts.google.com/o/oauth2/v2/auth",
    "TOKEN_URI": "https://oauth2.googleapis.com/token",
    "USERINFO_URI": "https://openidconnect.googleapis.com/v1/userinfo",
}


# === User Info / OpenID scopes ===
USERINFO_SCOPES = {
    "USERINFO_EMAIL": "https://www.googleapis.com/auth/userinfo.email",
    "USERINFO_PROFILE": "https://www.googleapis.com/auth/userinfo.profile",
    "OPENID": "openid",
    "EMAIL": "email",
    "PROFILE": "profile",
}

# === YouTube API scopes ===
YOUTUBE_SCOPES = {
    "YOUTUBE": "https://www.googleapis.com/auth/youtube",
    "YOUTUBE_UPLOAD": "https://www.googleapis.com/auth/youtube.upload",
    "YOUTUBE_READONLY": "https://www.googleapis.com/auth/youtube.readonly",
    "YOUTUBE_ANALYTICS": "https://www.googleapis.com/auth/yt-analytics.readonly",
    "YOUTUBE_FORCE_SSL": "https://www.googleapis.com/auth/youtube.force-ssl",
    "YOUTUBEPARTNER": "https://www.googleapis.com/auth/youtubepartner",
    "YOUTUBEPARTNER_CHANNEL_AUDIT": "https://www.googleapis.com/auth/youtubepartner-channel-audit",
}

# === Google Drive API scopes ===
DRIVE_SCOPES = {
    "DRIVE": "https://www.googleapis.com/auth/drive",
    "DRIVE_FILE": "https://www.googleapis.com/auth/drive.file",
    "DRIVE_READONLY": "https://www.googleapis.com/auth/drive.readonly",
    "DRIVE_METADATA": "https://www.googleapis.com/auth/drive.metadata",
    "DRIVE_METADATA_READONLY": "https://www.googleapis.com/auth/drive.metadata.readonly",
    "DRIVE_PHOTOS_READONLY": "https://www.googleapis.com/auth/drive.photos.readonly",
    "DRIVE_APPDATA": "https://www.googleapis.com/auth/drive.appdata",
    "DRIVE_SCRIPTS": "https://www.googleapis.com/auth/drive.scripts",
}

# === Gmail API scopes ===
GMAIL_SCOPES = {
    "GMAIL_READONLY": "https://www.googleapis.com/auth/gmail.readonly",
    "GMAIL_MODIFY": "https://www.googleapis.com/auth/gmail.modify",
    "GMAIL_COMPOSE": "https://www.googleapis.com/auth/gmail.compose",
    "GMAIL_SEND": "https://www.googleapis.com/auth/gmail.send",
    "GMAIL_INSERT": "https://www.googleapis.com/auth/gmail.insert",
    "GMAIL_LABELS": "https://www.googleapis.com/auth/gmail.labels",
    "GMAIL_METADATA": "https://www.googleapis.com/auth/gmail.metadata",
    "GMAIL_SETTINGS_BASIC": "https://www.googleapis.com/auth/gmail.settings.basic",
    "GMAIL_SETTINGS_SHARING": "https://www.googleapis.com/auth/gmail.settings.sharing",
}
