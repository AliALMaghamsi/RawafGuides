from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from models.user import User
from models.room import Room
from models.hotel import Hotel


async def get_hotels(db:Session , user:User):
    hotels = (
        db.query(Hotel)
        .join(Room)  
        .filter(Room.guide_id == user.id)
        .distinct()  
        .all()
    )
    return hotels



async def get_room_types(hotel_id: int, db: Session):
    types = db.query(Room.capacity).filter(Room.hotel_id == hotel_id).distinct().all()
    return [t[0] for t in types]



async def get_rooms(hotel_id:int , room_type:int , db:Session):
    rooms = (
        db.query(Room)
        .filter(Room.hotel_id == hotel_id , Room.capacity == room_type).all()
    )

    return rooms