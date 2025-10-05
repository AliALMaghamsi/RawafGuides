from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter , Depends , HTTPException , status, UploadFile , File
from sqlalchemy.orm import Session
from services.guide_services import process_guide_file
from core.sequrity import get_current_admin_user
from models.user import User
admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)



@admin_router.post("/upload_guides")
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = await process_guide_file(file=file , db=db)
    return response