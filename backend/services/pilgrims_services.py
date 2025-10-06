from fastapi import UploadFile
from schemas.pilgrim import PilgrimCreate
from models.pilgrim import Pilgrim
import pandas as pd 
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from io import BytesIO
from sqlalchemy.orm import Session
from utils import get_guide_id_by_passport, get_package_id_by_number
    

async def process_pilgrim_file(file:UploadFile ,db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []

    for index , row in df.iterrows():
        name = str(row["name"]).strip()
        passport_number = str(row["passport_number"]).strip()
        assigned_guide_passport = str(row["guide_passport"]).strip()
        package_number = str(row["package_number"]).strip()
        room_type = int(row["room_type"])
        group_id = int(row["group_id"])
        gender = str(row["gender"]).strip().lower()
         
    
        data = {
            "name":name,
            "passport_number":passport_number,
            "assigned_guide_passport":assigned_guide_passport,
            "package_number":package_number,
            "room_type":room_type,
            "group_id":group_id,
            "gender":gender
        }


        try:
            pilgrim = PilgrimCreate(**data)
            create_pilgrim(db=db , pilgrim_data= data)
        except ValidationError as ve:
            errors.append(f"Row:{index}: {ve}")

        except IntegrityError as ie :
            db.rollback()
            errors.append(f"Row:{index}: {ie}")
        except Exception as e :
            db.rollback()
            errors.append(f"Row: {index}: {e}")

        num_inserted = df.shape[0] - len(errors)

        return {
            "Inserted" : num_inserted,
            "failed" : len(errors),
            "errors": errors
        }



def create_pilgrim(db:Session , pilgrim_data:PilgrimCreate):
    guide_id = get_guide_id_by_passport(db=db, passport_number=pilgrim_data.assigned_guide_passport)
    package_id = get_package_id_by_number(db=db, package_number=pilgrim_data.package_number)
    check_pilgrim = db.query(Pilgrim).filter(Pilgrim.passport_number == pilgrim_data.passport_number)
    if check_pilgrim:
        raise ValidationError("pilgrim is added")

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