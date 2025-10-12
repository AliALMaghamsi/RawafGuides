from fastapi import UploadFile , HTTPException , status

import pandas as pd 
from io import BytesIO

from schemas.user import UserCreate , UserRead , UserUpload
from models.user import User
from models.hotel import Hotel
from models.room import Room

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from core.sequrity import get_password_hash


async def process_guides_file(file:UploadFile , db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []
    
    for index, row in df.iterrows():
        guide_name = str(row["guide_name"]).strip()
        try:
            guide = db.query(User).filter(User.name == guide_name).one_or_none()
            if guide:
                errors.append(f"Row {index}: Guide is already added")
                continue

            if not guide:
                hashed_password = get_password_hash(f"{guide_name}@2026")
                guide = User(
                    name = guide_name,
                    username = guide_name.replace(" ","_").lower(),
                    hashed_password = hashed_password,
                )
                db.add(guide)
                db.commit()
                db.refresh(guide)
            for i in range(1,4):
                hotel_col = f"hotel{i}"
                if pd.isna(row.get(hotel_col)):
                    continue
                
                hotel_name = str(row[hotel_col]).strip()
                rooms_2 = int(row[f"rooms_2s_h{i}"])
                rooms_3 = int(row[f"rooms_3s_h{i}"])
                rooms_4 = int(row[f"rooms_4s_h{i}"])
                

                hotel = db.query(Hotel).filter(Hotel.name == hotel_name).one_or_none()
                #hotel not found create it and add rooms 
                if not hotel:
                    
                    hotel_obj = Hotel(name =hotel_name)
                    db.add(hotel_obj)
                    db.commit()
                    db.refresh(hotel_obj)
                    last_room = db.query(Room).filter(Room.hotel_id == hotel_obj.id).order_by(Room.id.desc()).first()
                    room_counter = last_room.id + 1 if last_room else 1
                    
                    for cap, count in [(2, rooms_2), (3, rooms_3), (4, rooms_4)]:
                        for _ in range(count):
                            room = Room(
                                hotel_id=hotel_obj.id,
                                guide_id=guide.id,
                                capacity=cap,
                                current_capacity=0,
                                room_number=f"{hotel_name}-{room_counter}"
                            )
                            db.add(room)
                            room_counter += 1
                else:
                    last_room = db.query(Room).filter(Room.hotel_id == hotel.id).order_by(Room.id.desc()).first()
                    room_counter = last_room.id + 1 if last_room else 1
                    #if the hotel found add rooms to it 
                    for cap, count in [(2, rooms_2), (3, rooms_3), (4, rooms_4)]:
                        for _ in range(count):
                                room = Room(
                                    hotel_id=hotel.id,
                                    guide_id=guide.id,
                                    capacity=cap,
                                    current_capacity=0,
                                    room_number=f"{hotel_name}-{room_counter}"
                                )
                                db.add(room)
                                room_counter += 1

                db.commit()

        except IntegrityError as ie:
            db.rollback()
            errors.append(f"Row {index}: {ie}")
        
        except Exception as e :
            db.rollback()
            errors.append(f"Row {index}: {e}")
        
    num_inserted = df.shape[0] - len(errors)
    return {
        "Inserted": num_inserted,
        "Failed": len(errors),
        "Errors": errors
    }

async def create_guide_user(user_data:UserUpload , db:Session) -> UserRead:
    if db.query(User).filter(User.name == user_data.name).one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="User already added with that name")
    
    hashed_password = get_password_hash(f"{user_data.name}@2026")
    username = user_data.name.replace(" ","_").lower()
    create_user = UserCreate(name=user_data.name , role=user_data.role , username=username , hashed_password=hashed_password)
    
    user = User(**create_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)

