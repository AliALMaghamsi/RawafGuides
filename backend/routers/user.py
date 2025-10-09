from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter , Depends , HTTPException , status
from models.user import User
from models.hotel import Hotel
from models.room import Room
from sqlalchemy.orm import Session
from schemas.hotel import HotelRead
from core.sequrity import get_current_active_user
from schemas.pilgrim import PilgrimCreate , PilgrimRead

guide_router = APIRouter(
    prefix="/guide",
    tags=["guide"],
)


@guide_router.get("/hotels" , response_model=list[HotelRead])
async def get_hotels(user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    hotels = (
        db.query(Hotel)
        .join(Room)  # join Room table
        .filter(Room.guide_id == user.id)
        .distinct()  # unique hotels
        .all()
    )
    return hotels
