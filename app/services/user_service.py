# app/services/user_service.py
from typing import Optional, Literal, get_args

from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead

UserPropertyIdentifier = Literal["id", "email", "username", "token"]
ALLOWED_IDENTIFIERS = get_args(UserPropertyIdentifier)


class UserService:
    def __init__(self, db: Session):
        # store the session once…
        self.db = db
        # …and pass it into your repository
        self.repo = UserRepository(self.db)

    def list_users(self):
        return self.repo.list()

    def get_user_by_identifier(
            self,
            value: str | int,
            identifier: UserPropertyIdentifier = "id",
    ) -> Optional[UserRead]:
        if identifier not in ALLOWED_IDENTIFIERS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Identifier {identifier!r} is not allowed. "
                    f"Allowed: {ALLOWED_IDENTIFIERS}"
                ),
            )
        # delegate to repo…
        if identifier == "id":
            try:
                value = int(value)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Value {value!r} is not a valid integer ID.",
                )
            db_user = self.repo.get_by_id(value)
        elif identifier == "email":
            db_user = self.repo.get_by_email(value)
        elif identifier == "username":
            db_user = self.repo.get_by_username(value)
        elif identifier == "token":
            db_user = self.repo.get_by_token(value)
        else:
            db_user = None

        return None if db_user is None else UserRead.model_validate(db_user)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
