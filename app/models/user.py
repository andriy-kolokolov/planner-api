from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    username = Column(String, index=True, nullable=False, unique=True)
    email = Column(String, index=True, nullable=False, unique=True)
    token = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    email_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
