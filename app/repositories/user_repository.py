from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def list(self) -> list[type[User]]:
        return self.db.query(User).all()

    def create(self, user_in: UserCreate) -> User:
        # Hash password before storing
        hashed_password = get_password_hash(user_in.password)

        db_user = User(
            name=user_in.name,
            lastname=user_in.lastname,
            email=user_in.email,
            username=user_in.username,
            password=hashed_password,  # Store hashed password
            gender=user_in.gender,
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)

        # Hash password if it's being updated
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
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

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)