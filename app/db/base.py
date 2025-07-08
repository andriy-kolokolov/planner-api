from sqlalchemy.ext.declarative import declarative_base

from app.db.session import engine

Base = declarative_base()

def init_db():
    # This will look at all subclasses of Base and issue CREATE TABLE for each if not exists
    Base.metadata.create_all(bind=engine)

def drop_db():
    # This will drop all tables in the database
    Base.metadata.drop_all(bind=engine)
