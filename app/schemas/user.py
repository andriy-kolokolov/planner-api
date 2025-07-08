# Updated schemas (schemas/user.py)
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    username: str
    gender: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    gender: Optional[str] = None

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
