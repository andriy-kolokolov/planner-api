# routers/auth.py
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.auth import TokenData, LoginResponse, RegisterResponse
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService, get_auth_service, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["authentication"])

logger = logging.getLogger(__name__)


@router.post("/register", response_model=RegisterResponse)
def register_user(
        user_in: UserCreate,
        user_repository: UserRepository = Depends(get_user_repository)
):
    try:
        new_user = user_repository.get_by_username(user_in.username)
        if new_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_in.username} already registered"
            )
        user = user_repository.create(user_in)
        access_token = get_auth_service().create_user_token(user)
        return {
            "token": {
                "value": access_token,
                "type": "bearer"
            }, "user": user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = auth_service.create_user_token(user)
    return {
        "token": {
            "value": access_token,
            "type": "bearer"
        }, "user": user}


@router.get("/verify-token", response_model=TokenData)
def verify_token(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service)
):
    """Verify token and return user data."""
    return auth_service.validate_and_get_token_data(token)


@router.get("/current-user", response_model=UserRead)
def current_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.get_current_user(token)
