from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repo import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
        db: Session = Depends(get_db)
):
    user = UserRepository(db).get_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {form_data.username} not found")

    if not form_data.password == user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return {"access_token": '123123', "token_type": "bearer"}
