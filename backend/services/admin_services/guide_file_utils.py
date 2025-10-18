import hashlib
import json
import pandas as pd



from models.user import User
from models.room import Room

from core.sequrity import get_password_hash
from sqlalchemy.orm import Session

from .pilgrims_file_utils import unassign_pilgrims_from_room

## hash_row for each guide to check later if it's changed or not 
def compute_row_hash(row : dict) -> str:
    row_str = json.dumps(row , sort_keys=True , default=str)
    return hashlib.sha256(row_str.encode("utf-8")).hexdigest()





## create guide if it's not exist
async def create_guide_user(guide_name:str , hash_row:str, db:Session):
    
    username = guide_name.replace(" ","_").lower()
    hashed_password = get_password_hash(f"{username}@2026")
    guide = User(
        name = guide_name,
        username = username,
        hashed_password = hashed_password,
        hash_row = hash_row
        )
    db.add(guide)
    db.commit()
    db.refresh(guide)
    return guide

async def update_guide(db:Session,guide:User,guide_name:str):
    username = guide_name.replace(" ","_").lower()
    hashed_password = get_password_hash(f"{username}@2026")
    guide.name = guide_name
    guide.username = username
    guide.hashed_password = hashed_password

    db.commit()
    db.refresh(guide)
    



## get hotels columns to check how many hotels each guide have 
def get_hotels_columns(df:pd.DataFrame) ->list[str]:
    return [col for col in df.columns if col.lower().startswith("hotel")] 



def create_rooms(db:Session , guide_id:int , hotel_id:int , hotel_name:str , new_rooms:dict):
    last_room = db.query(Room).filter(Room.hotel_id == hotel_id).order_by(Room.id.desc()).first()
    room_counter = last_room.id + 1 if last_room else 1


   


    for cap , count in new_rooms.items():
        for _ in range(count):
            room = Room(
                hotel_id = hotel_id,
                guide_id = guide_id,
                capacity = cap,
                current_capacity =0,
                room_number =f"{hotel_name}-{room_counter}"
            )
            db.add(room)
            room_counter +=1
    
    db.commit()



def update_rooms(db: Session, guide_id: int, hotel_id: int, hotel_name: str, new_rooms: dict , warnings:list , index:int):
     for cap , new_count in new_rooms.items():
        existing_rooms = (
            db.query(Room)
            .filter(Room.hotel_id == hotel_id , Room.guide_id == guide_id , Room.capacity == cap)
            .all()
        )
        existing_count = len(existing_rooms)

        if existing_count < new_count:
            last_room = db.query(Room).filter(Room.hotel_id == hotel_id).order_by(Room.id.desc()).first()
            room_counter = last_room.id + 1 if last_room else 1
            for _ in range(new_count - existing_count):
                room = Room(
                hotel_id = hotel_id,
                guide_id = guide_id,
                capacity = cap,
                current_capacity =0,
                room_number =f"{hotel_name}-{room_counter}"
                )
                db.add(room)
                room_counter+=1
            db.commit()
        
        elif existing_count > new_count:
            remove_count = existing_count - new_count
            empty_rooms = [r for r in existing_rooms if r.current_capacity == 0]
            occupied_rooms = [r for r in existing_rooms if r.current_capacity > 0]


            for room in empty_rooms[:remove_count]:
                db.delete(room)
                remove_count -=1

            if remove_count > 0 and occupied_rooms:
                for room in occupied_rooms[:remove_count]:
                    unassign_pilgrims_from_room(db, room)
                    db.delete(room)
                    warnings.append(
                        f"Row:{index}: Guide '{guide_id}' at hotel '{hotel_name}': removed occupied room {room.room_number} — pilgrims unassigned."
                    )
            
            db.commit()
