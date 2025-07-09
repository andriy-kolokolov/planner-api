# app/api/v1/authentication.py
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv

from app.repositories.user_repository import UserRepository, get_user_repository
from app.schemas.auth import TokenData, LoginResponse, RegisteredResponse, TokenRead
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService, get_auth_service, oauth2_scheme
from app.services.user_service import get_user_service, UserService

router = APIRouter(prefix="/auth", tags=["authentication"])

logger = logging.getLogger(__name__)


@cbv(router)
class Auth:

    def __init__(
            self,
            user_repository: UserRepository = Depends(get_user_repository),
            user_service: UserService = Depends(get_user_service),
            auth_service: AuthService = Depends(get_auth_service)
    ):
        self.user_repository = user_repository
        self.user_service = user_service
        self.auth_service = auth_service

    @router.post("/register", response_model=RegisteredResponse)
    def register_user(self, user_in: UserCreate):
        """Register a new user and return access token."""
        try:
            # Check if user already exists
            existing_user = self.user_service.get_user_by_identifier(user_in.username, 'username')
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Username {user_in.username} already registered"
                )

            user = self.user_service.create_user(user_in)  # Returns UserRead
            # Pass the UserRead object directly, not a dict
            access_token = self.auth_service.create_user_token(user)

            # Create TokenRead instance
            token = TokenRead(value=access_token, type="bearer")

            # Return RegisteredResponse instance
            return RegisteredResponse(token=token, user=user)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Registration error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed"
            )

    @router.post("/login", response_model=LoginResponse)
    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        """Authenticate user and return access token."""
        # authenticate_user returns a User model, not UserRead
        db_user = self.auth_service.authenticate_user(form_data.username, form_data.password)
        access_token = self.auth_service.create_user_token(db_user)

        # (db_user) Model → (UserRead) Schema Conversions
        user_read = UserRead.model_validate(db_user)

        # Create TokenRead instance
        token = TokenRead(value=access_token, type="bearer")

        # Return LoginResponse instance
        return LoginResponse(token=token, user=user_read)

    @router.post("/token")
    async def token(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user_read = self.auth_service.authenticate_user(form_data.username, form_data.password)
        access_token = self.auth_service.create_user_token(user_read)

        return {"access_token": access_token, "token_type": "bearer"}

    @router.get("/verify-token", response_model=TokenData)
    def verify_token(self, token: str = Depends(oauth2_scheme)):
        """Verify token and return user data."""
        return self.auth_service.validate_and_get_token_data(token)

    @router.get("/current-user", response_model=UserRead)
    def current_user(self, token: str = Depends(oauth2_scheme)):
        """Get current authenticated user."""
        return self.auth_service.get_current_user(token)