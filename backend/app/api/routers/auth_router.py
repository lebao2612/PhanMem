from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from app.dtos import AuthDTO
from app.schemas.responses import SuccessResponse
from app.dependencies import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/google/oauth")
def redirect_to_google_oauth():
    """
    Redirect user to Google OAuth authorization URL with basic scopes.
    """
    url = auth_service.get_google_oauth_url()
    from config import settings
    print("REDIRECT_URI:", settings.GOOGLE_REDIRECT_URI)
    return RedirectResponse(url)


@router.get("/google/oauth/extend")
def redirect_to_google_oauth_extended():
    """
    Redirect user to Google OAuth authorization URL with extended scopes (e.g. YouTube).
    """
    url = auth_service.get_google_oauth_extend_url()
    return RedirectResponse(url)


@router.get("/google/callback", response_model=SuccessResponse[AuthDTO])
def google_oauth_callback(
    code: str = Query(..., description="Authorization code returned from Google OAuth"),
    state: str = Query(None, description="Optional state value, e.g., 'retry' to force extended scope")
):
    """
    Handle callback from Google OAuth. Exchange code for tokens and return user info.
    If scope is insufficient and `state=retry`, redirect to extended scope OAuth URL.
    """
    retry = (state == "retry")
    auth_dto = auth_service.handle_google_oauth_callback(code=code, retry=retry)
    if auth_dto:
        return SuccessResponse(data=auth_dto)

    # If retry required (e.g., need YouTube access), redirect to extended scopes
    extend_url = auth_service.get_google_oauth_extend_url()
    return RedirectResponse(url=extend_url)