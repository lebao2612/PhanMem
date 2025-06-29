from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services import AuthService
from app.dtos import AuthDTO
from app.schemas.responses import SuccessResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

# This endpoint is used to redirect to Google OAuth
@router.get("/google/oauth")
def redirect_to_google_oauth():
    url = AuthService.get_google_oauth_url(
        prompt="select_account",
        include_granted_scopes=False
        )
    return RedirectResponse(url)

# This endpoint is used to redirect to Google OAuth with extended scopes
@router.get("/google/oauth/extend")
def redirect_to_google_oauth_extended():
    url = AuthService.get_google_oauth_url(
        prompt="consent",
        include_granted_scopes=True)
    return RedirectResponse(url)

# This endpoint handles the callback from Google OAuth after user authorization
@router.get("/google/callback", response_model=SuccessResponse[AuthDTO])
def google_oauth_callback(code: str):
    auth_dto = AuthService.handle_google_oauth_callback(code)
    return SuccessResponse(data=auth_dto)