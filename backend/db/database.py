from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings



Database_url = settings.DATABSE_URL
connect_args = {"check_same_thread":False}

engine = create_engine(Database_url,connect_args= connect_args)
SessionLocal = sessionmaker(autocommit=False,autoflush=False , bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind = engine)