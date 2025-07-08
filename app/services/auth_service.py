# services/auth_service.py
import logging
from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData
from app.schemas.user import UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> User:
        """Register a new user."""
        existing_user = self.user_repository.get_by_username(user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        return self.user_repository.create(user_in)

    def authenticate_user(self, username: str, password: str) -> User:
        """Authenticate user with username and password."""
        user = self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username {username} not found"
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def create_user_token(self, user: User) -> str:
        """Create JWT token for authenticated user."""
        exp = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=exp
        )
        return access_token

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        """Get current user from JWT token."""
        token_data = self.validate_and_get_token_data(token)
        user = self.user_repository.get_by_username(token_data.username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    def get_current_active_user(self, current_user: User = Depends(get_current_user)) -> User:
        """Get current active user."""
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user

    def validate_and_get_token_data(self, token: str) -> TokenData:
        """Validate token and return token data if valid."""
        # First validate the token format
        self.validate_token_format(token)

        # Then decode and validate token content
        try:
            # decode_token should return the decoded payload
            token_payload = decode_token(token)

            # Verify user exists
            user = self.user_repository.get_by_username(token_payload.username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return token_payload

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired. Please login again to get a new token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTClaimsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or secret key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except HTTPException:
            # Re-raise HTTP exceptions (like user not found)
            raise
        except Exception as e:
            logger.error(f"Unexpected error validating token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def validate_token_format(self, token: str):
        """Validate token format before attempting to decode."""
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not isinstance(token, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token must be a string",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Handle empty string, whitespace-only strings, and string "null"/"none"
        if not token.strip() or token.lower() in ["null", "none"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        """Get current user from token - useful for other endpoints."""
        token_data = self.validate_and_get_token_data(token)
        user = self.user_repository.get_by_username(token_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)
