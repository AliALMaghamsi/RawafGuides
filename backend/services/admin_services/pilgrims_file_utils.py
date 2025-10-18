



from sqlalchemy.orm import Session
from models.pilgrim import Pilgrim
from models.room import Room




def unassign_pilgrims_from_room(db:Session , room:Room):
    pilgrims = (
        db.query(Pilgrim)
        .filter(
            (Pilgrim.room_h1_id == room.id) |
            (Pilgrim.room_h2_id == room.id) |
            (Pilgrim.room_h3_id == room.id)
        )
        .all()
    )

    for pilgrim in pilgrims:
        if pilgrim.room_h1_id == room.id:
            pilgrim.room_h1_id = None
        if pilgrim.room_h2_id == room.id:
            pilgrim.room_h2_id = None
        
        if pilgrim.room_h3_id == room.id:
            pilgrim.room_h3_id = None
    db.commit()