from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import app_settings

engine = create_engine(app_settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
