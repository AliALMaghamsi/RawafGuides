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

guide_router = APIRouter(
    prefix="/guide",
    tags=["guide"],
)


@guide_router.get("/hotels/" , response_model=list[HotelRead])
async def get_hotels(user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    hotels = (
        db.query(Hotel)
        .join(Room)  
        .filter(Room.guide_id == user.id)
        .distinct()  
        .all()
    )
    return hotels

@guide_router.get("/hotels/{hotel_id}/room-types/")
def get_room_types(hotel_id: int, db: Session = Depends(get_db)):
    types = db.query(Room.capacity).filter(Room.hotel_id == hotel_id).distinct().all()
    return [t[0] for t in types]



@guide_router.get("/hotels/{hotel_id}/rooms/{room_type}",response_model=list[RoomRead])
async def get_rooms(hotel_id:int , room_type:int ,user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    rooms = (
        db.query(Room)
        .filter(Room.hotel_id == hotel_id , Room.capacity == room_type).all()
    )

    return rooms


@guide_router.get("/hotels/rooms/{room_type}/pilgrims" , response_model=list[PilgrimRead])
async def get_rooms(room_type:int ,user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    pilgrims = (
        db.query(Pilgrim)
        .filter(Pilgrim.guide_id == user.id , Pilgrim.room_type == room_type )
        .all()
    )
    return pilgrims


@guide_router.put("/pilgrims/{pilgrim_id}/")
async def update_pilgrim_room(pilgrim_id :int ,data:PilgrimUpdateRoom,user:User = Depends(get_current_active_user) , db:Session = Depends(get_db)):
    pilgrim = db.query(Pilgrim).filter(Pilgrim.id == pilgrim_id).first()
    if not pilgrim:
        raise HTTPException(status_code=404, detail="Pilgrim not found")

    
    
    if data.room_id:
        
        room = (
            db.query(Room)
            .filter(Room.id == data.room_id, Room.guide_id == user.id)
            .first()
        )
        
        if not room:
            raise HTTPException(status_code=403, detail="Room not accessible")
        
        if room.current_capacity == room.capacity:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED , detail="the room is full")
        
        pilgrim.room_id = room.id
        room.current_capacity +=1
        db.commit()
        db.refresh(room)
        db.refresh(pilgrim)
    else:
        if pilgrim.room_id:
            room = db.query(Room).filter(Room.id == pilgrim.room_id).first()
            pilgrim.room_id = None
            room.current_capacity -=1
            db.commit()
            db.refresh(room)
            db.refresh(pilgrim)
        

    
    

    return {
        "id": pilgrim.id,
        "name": pilgrim.name,
        "room_id": pilgrim.room_id,
        "message": "Pilgrim assignment updated successfully",
    }