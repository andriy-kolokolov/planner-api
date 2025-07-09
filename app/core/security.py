# core/security.py
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings
from app.schemas.auth import TokenData

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")
settings = get_settings()
logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token with proper timezone handling."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.debug(payload)

        username: str = payload.get("username")
        user_id: int = payload.get("user_id")
        exp: datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)

        if username is None:
            raise JWTError("Token missing username")

        token_data = TokenData(username=username, user_id=user_id, expires_at=exp)
        return token_data
    except JWTError:
        raise JWTError("Invalid token")
