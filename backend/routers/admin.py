from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter , Depends , HTTPException , status, UploadFile , File
from sqlalchemy.orm import Session
from services.guide_services import process_guide_file , create_guide_user
from services.package_services import process_package_file
from services.pilgrims_services import process_pilgrim_file , create_pilgrim
from schemas.user import GuideRead, GuideDB , GuideUPload
from core.sequrity import get_current_admin_user
from schemas.pilgrim import PilgrimCreate , PilgrimRead
from models.user import User
admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@admin_router.post("/upload_packages" ,tags=["Packages"])
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = await process_package_file(file=file , db=db)
    return response

@admin_router.post("/upload_guides" , tags=["Guides"])
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = await process_guide_file(file=file , db=db)
    return response

@admin_router.post("/create/guide", response_model=GuideRead , tags=["Guides"])
def create_user(guide_data:GuideUPload,db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = create_guide_user(db=db , guide_data=guide_data)
    return response

@admin_router.post("/upload_pirlgrims" , tags=["Pilgrims"])
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = await process_pilgrim_file(file=file , db=db)
    return response



@admin_router.post("/create/pilgrim", response_model=PilgrimRead, tags=["Pilgrims"])
def add_pilgrim(pilgrim_data:PilgrimCreate,db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = create_pilgrim(db=db , pilgrim_data=pilgrim_data)
    return response
