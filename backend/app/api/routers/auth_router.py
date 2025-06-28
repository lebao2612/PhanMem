from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.services import AuthService
from app.dtos import AuthDTO
from app.schemas.responses import SuccessResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/google/oauth")
def redirect_to_google_oauth():
    url = AuthService.get_google_oauth_url()
    return RedirectResponse(url)

    
@router.get("/google/callback", response_model=SuccessResponse[AuthDTO])
def google_oauth_callback(code: str):
    auth_dto = AuthService.handle_google_oauth_callback(code)
    return SuccessResponse(data=auth_dto)