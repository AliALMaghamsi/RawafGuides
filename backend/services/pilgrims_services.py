from fastapi import UploadFile , HTTPException , status
from schemas.pilgrim import PilgrimCreate , PilgrimRead
from models.pilgrim import Pilgrim
import pandas as pd 
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from io import BytesIO
from sqlalchemy.orm import Session
from .utils import get_guide_id_by_passport, get_package_id_by_number
    

async def process_pilgrim_file(file:UploadFile ,db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []
    inserted_count = 0
    pending = []
    BATCH_SIZE = 100

    for index , row in df.iterrows():
        try:
            data = {
                "name": str(row["name"]).strip(),
                "passport_number": str(row["passport_number"]).strip(),
                "assigned_guide_passport": str(row["guide_passport"]).strip(),
                "package_number": str(row["package_number"]).strip(),
                "room_type": int(row["room_type"]),
                "group_id": int(row["group_id"]),
                "gender": normalize_gender(row["gender"])

            }
            
            



            pilgrim_data = PilgrimCreate(**data)
            guide_id = get_guide_id_by_passport(db=db, passport_number=pilgrim_data.assigned_guide_passport)
            package_id = get_package_id_by_number(db=db, package_number=pilgrim_data.package_number)
            if not guide_id:
                errors.append(f"Row {index+1}: Guide passport not found ({pilgrim_data.assigned_guide_passport})")
                continue
            
            if not package_id:
                errors.append(f"Row {index+1}: Package number not found ({pilgrim_data.package_number})")
                continue
            
            existing = db.query(Pilgrim).filter(Pilgrim.passport_number == pilgrim_data.passport_number).first()
            if existing:
                errors.append(f"Row {index+1}: Pilgrim already exists ({pilgrim_data.passport_number})")
                continue
            
            pilgrim = Pilgrim(
                name=pilgrim_data.name,
                passport_number=pilgrim_data.passport_number,
                assigned_guide_id=guide_id,
                package_id=package_id,
                room_type=pilgrim_data.room_type,
                group_id=pilgrim_data.group_id,
                gender=pilgrim_data.gender,
            )
           
            pending.append(pilgrim)
            if len(pending) >= BATCH_SIZE:
                db.add_all(pending)
                db.commit()
                inserted_count += len(pending)
                pending.clear()  # empty list for next batch

        except ValueError as ve:
            errors.append(f"Row {index}: {ve}")
        except IntegrityError as ie:
            db.rollback()
            errors.append(f"Row {index}: Database integrity error ({ie.orig})")
        except Exception as e:
            db.rollback()
            errors.append(f"Row {index}: Unexpected error ({e})")
    if pending:
        db.add_all(pending)
        db.commit()
        inserted_count += len(pending)

    return {
        "Inserted": inserted_count,
        "Failed": len(errors),
        "Errors": errors,
    }

        

       

    



def create_pilgrim(db:Session , pilgrim_data:PilgrimCreate):
    guide_id = get_guide_id_by_passport(db=db, passport_number=pilgrim_data.assigned_guide_passport)
    if not guide_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="guide id not found")
    package_id = get_package_id_by_number(db=db, package_number=pilgrim_data.package_number)
    if not package_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="package id not found")
    check_pilgrim = db.query(Pilgrim).filter(Pilgrim.passport_number == pilgrim_data.passport_number).first()
    if check_pilgrim:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="pilgrim allready added")

    pilgrim = Pilgrim(
        name = pilgrim_data.name,
        passport_number = pilgrim_data.passport_number,
        assigned_guide_id = guide_id,
        package_id = package_id,
        room_type = pilgrim_data.room_type,
        group_id = pilgrim_data.group_id,
        gender = pilgrim_data.gender
    )
    db.add(pilgrim)
    db.commit()
    db.refresh(pilgrim)

    return PilgrimRead.model_validate(pilgrim)




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
