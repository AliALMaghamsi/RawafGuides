from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter , Depends , HTTPException , status, UploadFile , File
from sqlalchemy.orm import Session
from services.admin_services.guide_services import process_guides_file , create_guide_user
from services.admin_services.pilgrims_services import process_pilgrims_file
from schemas.user import UserCreate , UserRead , UserUpload

from core.sequrity import get_current_admin_user
from schemas.pilgrim import PilgrimCreate , PilgrimRead
from models.user import User
admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)



@admin_router.post("/upload/guides/" , tags=["Guides"])
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = await process_guides_file(file=file , db=db)
    return response
    
@admin_router.post("/create/guide/" , tags=["Guides"] , response_model=UserRead)
async def create_guide(user_data:UserUpload , db:Session=Depends(get_db), current_user:User = Depends(get_current_admin_user)):
    response = await create_guide_user(user_data=user_data , db=db)
    return response


@admin_router.post("upload/pilgrims/" , tags=["pilgrims"])
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = await process_pilgrims_file(file=file , db=db)
    return response