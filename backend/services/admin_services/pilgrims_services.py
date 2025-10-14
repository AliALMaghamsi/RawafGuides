from fastapi import UploadFile , HTTPException , status

import pandas as pd 
from io import BytesIO


from models.user import User
from models.pilgrim import Pilgrim
from models.room import Room
from models.hotel import Hotel

from sqlalchemy.orm import Session
from sqlalchemy import func , select , or_
from sqlalchemy.exc import IntegrityError





async def process_pilgrims_file(file:UploadFile , db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []
    
    for index, row in df.iterrows():
        
        try:
            name = str(row["name"]).strip()
            passport_number = str(row["passport_number"]).strip()
            guide_name = str(row["guide_name"]).strip()
            room_type_h1 = int(row["room_type_h1"])
            room_type_h2 = int(row["room_type_h2"])
            room_type_h3 = int(row["room_type_h3"]) if not pd.isna(row["room_type_h3"]) else None
            group_number = int(row["group_number"])
            gender= normalize_gender(row["gender"])
            hotel1 = str(row["hotel1"]).strip()
            hotel2 = str(row["hotel2"]).strip()
            hotel3 = str(row["hotel3"]).strip() if  not pd.isna(row["hotel3"]) else None


            guide = db.query(User).filter(User.name == guide_name).one_or_none()
            if not guide:
                errors.append(f"Row {index+1}: Guide '{guide_name}' not found.")
                continue

            hotel1_id = db.query(Hotel.id).filter(Hotel.name == hotel1).one_or_none()
            hotel2_id = db.query(Hotel.id).filter(Hotel.name == hotel2).one_or_none()
            hotel3_id = db.query(Hotel.id).filter(Hotel.name == hotel3).one_or_none()
            if hotel3_id:
                hotel3_id = hotel3_id[0]

            check_pilgrim = db.query(Pilgrim).filter(Pilgrim.passport_number == passport_number).one_or_none()
            if check_pilgrim:
                errors.append(f"Row {index+1}: User with passport '{passport_number}' already has been added.")
                continue

            pilgrim = Pilgrim(
                name = name,
                passport_number = passport_number,
                room_type_h1 = room_type_h1,
                room_type_h2 = room_type_h2,
                room_type_h3 = room_type_h3,
                group_number = group_number,
                gender = gender,
                guide_id = guide.id,
                h1_id = hotel1_id[0],
                h2_id = hotel2_id[0],
                h3_id = hotel3_id,
            )
            db.add(pilgrim)
            

        except IntegrityError as ie:
            db.rollback()
            errors.append(f"Row {index}: {ie}")
        
        except Exception as e :
            db.rollback()
            errors.append(f"Row {index}: {e}")
        
    num_inserted = df.shape[0] - len(errors)
    db.commit()
    assign_room_by_group_number(db=db)
    
    return {
        "Inserted": num_inserted,
        "Failed": len(errors),
        "Errors": errors
    }




def normalize_gender(value:str):
    if not value:
        return None
    value = str(value).strip().upper()
    if value in ["M", "MALE"]:
        return "male"
    elif value in ["F", "FEMALE"]:
        return "female"
    else:
        raise ValueError(f"Invalid gender value: {value}")
    

def assign_room_by_group_number(db:Session):
    groups = (
        db.query(Pilgrim.group_number)
        .filter(
            or_(
                Pilgrim.room_type_h1 == 2,
                Pilgrim.room_type_h2 == 2,
                Pilgrim.room_type_h3 == 2,
            )
        )
        .group_by(Pilgrim.group_number)
        .having(func.count(Pilgrim.id) == 2)
        .all()
    )

    groups = [gr[0] for gr in groups]
    print(f"✅ Found {len(groups)} groups with exactly 2 pilgrims")

    for grn in groups:
        pilgrims = (
            db.query(Pilgrim)
            .filter(Pilgrim.group_number == grn)
            .all()
        )

        if len(pilgrims) != 2:
            continue  # skip if something unexpected

        p1, p2 = pilgrims
        print(f"\n🟦 Assigning Group {grn} (Pilgrims: {p1.id}, {p2.id})")

        # Step 2: For each hotel column (h1, h2, h3)
        for i in range(1, 4):
            hotel_id_attr = f"h{i}_id"
            room_type_attr = f"room_type_h{i}"
            room_id_attr = f"room_h{i}_id"

            hotel_id = getattr(p1, hotel_id_attr)
            room_type_1 = getattr(p1, room_type_attr)
            room_type_2 = getattr(p2, room_type_attr)

            if (
                hotel_id
                and hotel_id == getattr(p2, hotel_id_attr)
                and room_type_1 == 2
                and room_type_2 == 2
            ):
                # Step 3: find an available room for that hotel/guide
                room = (
                    db.query(Room)
                    .filter(
                        Room.hotel_id == hotel_id,
                        Room.guide_id == p1.guide_id,
                        Room.capacity == 2,
                        Room.current_capacity == 0,
                    )
                    .first()
                )

                if room:
                    # Step 4: Assign both pilgrims to this room
                    setattr(p1, room_id_attr, room.id)
                    setattr(p2, room_id_attr, room.id)

                    room.current_capacity += 2  # mark room as full

                    db.add_all([p1, p2, room])
                    db.flush()  # make sure next loop sees changes

    db.commit()
    
