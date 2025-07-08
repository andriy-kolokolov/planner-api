from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.user_service import get_user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self):
        self.user_service = Depends(get_user_service)
