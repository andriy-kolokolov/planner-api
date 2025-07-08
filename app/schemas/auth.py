from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import UserRead


class TokenData(BaseModel):
    """Token data model for validation."""
    username: str
    user_id: int
    expires_at: datetime


class TokenRead(BaseModel):
    value: str
    type: str


class LoginResponse(BaseModel):
    token: TokenRead
    user: UserRead


class RegisterResponse(BaseModel):
    token: TokenRead
    user: UserRead
