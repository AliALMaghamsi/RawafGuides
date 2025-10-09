from fastapi import UploadFile , HTTPException , status

import pandas as pd 
from io import BytesIO


from models.user import User
from models.pilgrim import Pilgrim

from sqlalchemy.orm import Session
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
            room_type = int(row["room_type"])
            group_number = int(row["group_number"])
            gender= normalize_gender(row["gender"])


            guide = db.query(User).filter(User.name == guide_name).one_or_none()
            if not guide:
                errors.append(f"Row {index+1}: Guide '{guide_name}' not found.")
                continue

            check_pilgrim = db.query(Pilgrim).filter(Pilgrim.passport_number == passport_number).one_or_none()
            if check_pilgrim:
                errors.append(f"Row {index+1}: User with passport '{passport_number}' already has been added.")
                continue

            pilgrim = Pilgrim(
                name = name,
                passport_number = passport_number,
                room_type = room_type,
                group_number = group_number,
                gender = gender,
                guide_id = guide.id
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