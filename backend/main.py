from contextlib import asynccontextmanager
from fastapi import FastAPI , UploadFile , Depends , File
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from db.database import get_db , create_tables , SessionLocal
from services.guide_services import process_guide_file
from passlib import hash
from models.user import User , Role
from core.config import settings

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    try:
        db = SessionLocal()
        admin_exists = db.query(User).filter(User.role == Role.admin).first()
        if not admin_exists:
            username = settings.AMDIN_USERNAME
            password = settings.AMDIN_PASSWORD
            hashed_password = hash.bcrypt.hash(password)
            admin = User(
                name = "Admin",
                username= username,
                hashed_password = hashed_password,
                role = Role.admin
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
    finally:
        db.close()



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/api/upload_guides")
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) ):
    response = process_guide_file(file=file , db=db)
    return response