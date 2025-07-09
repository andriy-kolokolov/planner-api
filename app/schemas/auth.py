# app/schemas/auth.py
from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel, field_validator

from app.schemas.user import UserRead


class TokenData(BaseModel):
    """Token data model for validation."""
    username: str
    user_id: int
    expires_at: datetime


class TokenRead(BaseModel):
    value: str
    type: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenRead":
        """Create TokenRead from dictionary."""
        return cls(**data)


class LoginResponse(BaseModel):
    token: TokenRead
    user: UserRead

    @field_validator('token', mode='before')
    def validate_token(cls, v):
        """Convert dict to TokenRead if needed."""
        if isinstance(v, dict):
            return TokenRead(**v)
        return v


class RegisteredResponse(BaseModel):
    token: TokenRead
    user: UserRead

    @field_validator('token', mode='before')
    def validate_token(cls, v):
        """Convert dict to TokenRead if needed."""
        if isinstance(v, dict):
            return TokenRead(**v)
        return v