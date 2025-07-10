from .internal_depends import (
    mongo_conn,

    user_repository,
    video_repository,

    jwt_service,
    auth_service,
    user_service,
    video_service,
    youtube_service,
    generator_service
)

from .external_depends import (
    cloudinary_client,
    
    gemini_client,
    google_tts_client,
    stable_diffusion_client,
    
    google_oauth_client,
    youtube_auth,
    youtube_client,
)