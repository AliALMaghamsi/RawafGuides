from sqlalchemy.orm import Session
from sqlalchemy import or_ , and_
from fastapi import HTTPException, status

from models.pilgrim import Pilgrim
from models.room import Room
from models.user import User
from schemas.pilgrim import PilgrimUpdateRoom




async def update_room(db:Session ,hotel_id:int, pilgrim_id:int , data:PilgrimUpdateRoom , user:User):
    
   
    pilgrim = db.query(Pilgrim).filter(Pilgrim.id == pilgrim_id).first()
    if not pilgrim:
        raise HTTPException(status_code=404, detail="Pilgrim not found")

    # Determine which room_hX_id to update
    if pilgrim.h1_id == hotel_id:
        room_field = "room_h1_id"
    elif pilgrim.h2_id == hotel_id:
        room_field = "room_h2_id"
    elif pilgrim.h3_id == hotel_id:
        room_field = "room_h3_id"
    else:
        raise HTTPException(status_code=400, detail="Pilgrim not linked to this hotel")

    new_room_id = data.room_id
    current_room_id = getattr(pilgrim, room_field)

    # Remove from current room
    if not new_room_id:
        if current_room_id:
            old_room = db.query(Room).filter(Room.id == current_room_id).first()
            if old_room:
                old_room.current_capacity -= 1
        setattr(pilgrim, room_field, None)
        db.commit()
        db.refresh(pilgrim)
        return {"message": "Pilgrim removed from room"}

    # Assign new room
    room = db.query(Room).filter(Room.id == new_room_id, Room.guide_id == user.id).first()
    if not room:
        raise HTTPException(status_code=403, detail="Room not accessible")
    if room.current_capacity >= room.capacity:
        raise HTTPException(status_code=405, detail="Room is full")

    # Free old room if assigned
    if current_room_id and current_room_id != new_room_id:
        old_room = db.query(Room).filter(Room.id == current_room_id).first()
        if old_room:
            old_room.current_capacity -= 1

    # Update pilgrim and room
    setattr(pilgrim, room_field, new_room_id)
    room.current_capacity += 1

    db.commit()
    db.refresh(pilgrim)
    return {"message": f"Pilgrim assigned to room {room.room_number}"}



async def get_pilgrims(hotel_id: int, room_type: int, user: User, db: Session):
    # Fetch pilgrims for the guide and matching hotel + room_type
    pilgrims = (
        db.query(Pilgrim)
        .filter(
            Pilgrim.guide_id == user.id,
            or_(
                Pilgrim.h1_id == hotel_id,
                Pilgrim.h2_id == hotel_id,
                Pilgrim.h3_id == hotel_id,
            ),
            # Only fetch pilgrims for this room_type and hotel
            or_(
                and_(Pilgrim.h1_id == hotel_id, Pilgrim.room_type_h1 == room_type),
                and_(Pilgrim.h2_id == hotel_id, Pilgrim.room_type_h2 == room_type),
                and_(Pilgrim.h3_id == hotel_id, Pilgrim.room_type_h3 == room_type),
            )
        )
        .all()
    )

    return pilgrims