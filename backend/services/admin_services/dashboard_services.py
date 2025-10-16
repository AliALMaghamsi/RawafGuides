from fastapi import status , HTTPException

from sqlalchemy.orm import Session

from models.hotel import Hotel
from models.pilgrim import Pilgrim
from models.room import Room

from schemas.hotel import HotelRead
from schemas.room import RoomRead
from schemas.pilgrim import PilgrimRead




async def get_hotels(db:Session):
    return db.query(Hotel).all()



    