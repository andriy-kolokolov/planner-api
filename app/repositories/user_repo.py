from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_token(self, token: str) -> Optional[User]:
        return self.db.query(User).filter(User.token == token).first()

    def list(self) -> list[type[User]]:
        return self.db.query(User).all()

    def create(self, user_in: UserCreate) -> User:
        db_user = User(
            name=user_in.name,
            lastname=user_in.lastname,
            email=user_in.email,
            password=user_in.password,  # todo HASH
            gender=user_in.gender
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        for field, value in user_in.model_dump(exclude_unset=True).items():
            setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        self.db.delete(db_user)
        self.db.commit()
        return True
