from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



database_filename = "rawafguides.db"
Database_url = f"sqlite:///{database_filename}"
connect_args = {"check_same_thread":False}

engine = create_engine(Database_url,connect_args= connect_args)
SessionLocal = sessionmaker(autocommit=False,autoflush=False , bind=engine)

Base = declarative_base()