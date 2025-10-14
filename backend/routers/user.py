from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter , Depends , HTTPException , status
from models.user import User
from models.hotel import Hotel
from models.pilgrim import Pilgrim
from models.room import Room
from sqlalchemy.orm import Session
from schemas.hotel import HotelRead
from schemas.room import RoomRead
from schemas.pilgrim import PilgrimRead , PilgrimUpdateRoom
from core.sequrity import get_current_active_user
from schemas.pilgrim import PilgrimCreate , PilgrimRead
from services.guide_services.pilgrims_services import update_room , get_pilgrims
from services.guide_services.hotels_services import get_hotels ,get_room_types , get_rooms
from services.admin_services.pilgrims_services import assign_room_by_group_number
guide_router = APIRouter(
    prefix="/guide",
    tags=["guide"],
)


@guide_router.get("/hotels/" , response_model=list[HotelRead])
async def read_hotels(user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    
    response = await get_hotels(db=db , user=user)
    return response
    

@guide_router.get("/hotels/{hotel_id}/room-types/")
async def read_room_types(hotel_id: int, db: Session = Depends(get_db) , user:User = Depends(get_current_active_user)):
    response = await get_room_types(hotel_id=hotel_id , db=db)
    return response



@guide_router.get("/hotels/{hotel_id}/rooms/{room_type}",response_model=list[RoomRead])
async def read_rooms(hotel_id:int , room_type:int ,user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    response = await get_rooms(hotel_id=hotel_id , room_type=room_type , db=db)
    
    return response


@guide_router.get("/hotels/{hotel_id}/rooms/{room_type}/pilgrims" , response_model=list[PilgrimRead])
async def read_pilgrims(hotel_id:int,room_type:int ,user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    response = await get_pilgrims(hotel_id=hotel_id,room_type=room_type , user=user , db=db)
    return response


@guide_router.put("/update/pilgrims/{hotel_id}/{pilgrim_id}/")
async def update_pilgrim_room(hotel_id:int,pilgrim_id :int ,data:PilgrimUpdateRoom,user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    response = await update_room(db=db ,hotel_id=hotel_id, pilgrim_id=pilgrim_id , data=data , user=user)
    return response