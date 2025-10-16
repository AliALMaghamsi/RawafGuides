from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter , Depends , HTTPException , status, UploadFile , File
from sqlalchemy.orm import Session
from services.admin_services.guide_services import process_guides_file , create_guide_user
from services.admin_services.pilgrims_services import process_pilgrims_file
from services.admin_services.dashboard_services import get_hotels
from schemas.user import UserCreate , UserRead , UserUpload
from services.admin_services.file_maker import download_pilgrims
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


@admin_router.post("/upload/pilgrims/" , tags=["pilgrims"])
async def Upload_file(file : UploadFile = File(...) , db : Session = Depends(get_db) , current_user:User = Depends(get_current_admin_user)):
    response = await process_pilgrims_file(file=file , db=db)
    return response

@admin_router.get("/download/excelfile/")
async def download_file(db:Session = Depends(get_db) , current_user : User = Depends(get_current_admin_user)):
    response = await download_pilgrims(db=db)
    return response


@admin_router.get("/dashboard/read/hotels/")
async def read_hotels(db:Session = Depends(get_db), ):
    """
    will return all the hotels in the db
    """
    return await get_hotels(db=db)
    

@admin_router.get("/dashboard/read/hotels/{hotel_id}/")
async def get_hotels_period(hotels,db:Session = Depends(get_db), current_user:User = Depends(get_current_admin_user)):
    """
    will return all the periods of the hotel has been choosing if it was the first hotel , second , or third
    """
    pass
