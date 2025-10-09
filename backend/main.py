from contextlib import asynccontextmanager
from fastapi import FastAPI , UploadFile , Depends , File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from db.database import get_db , create_tables , SessionLocal
from models.hotel import Hotel
from models.pilgrim import Pilgrim
from models.room import Room 
from core.sequrity import get_password_hash
from models.user import User , Role
from core.config import settings
from routers.auth import auth_router
from routers.admin import admin_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    try:
        db = SessionLocal()
        admin_exists = db.query(User).filter(User.role == Role.admin).first()
        if not admin_exists:
            username = settings.ADMIN_USERNAME
            password = settings.ADMIN_PASSWORD
            hashed_password = get_password_hash(password)
            admin = User(
                name = "Admin",
                username= username,
                hashed_password = hashed_password,
                role = Role.admin
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        yield
    finally:
        db.close()



app = FastAPI(lifespan= lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router , prefix="/api")
app.include_router(admin_router , prefix="/api")

@app.get("/")
def health_check():
    return "api:Ok"