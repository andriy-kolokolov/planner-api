from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    gender: Optional[str]
    is_active: Optional[bool]


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    email_verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    is_active: Optional[bool]
    email_verified_at: Optional[datetime]

class UserPassword(UserBase):
    password: str