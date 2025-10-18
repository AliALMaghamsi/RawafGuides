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

from .guide_file_utils import compute_row_hash , create_guide_user,update_guide , get_hotels_columns , create_rooms , update_rooms


async def process_guides_file(file:UploadFile , db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []
    warnings = []
    
    for index, row in df.iterrows():
        guide_name = str(row["guide_name"]).strip()

        try:
            hash_row = compute_row_hash(row.to_dict())
            guide = db.query(User).filter(User.name == guide_name).one_or_none()
            if not guide:
                guide = await create_guide_user(guide_name=guide_name ,hash_row=hash_row , db=db)
            
                
                for col in get_hotels_columns(df=df):
                    
                    hotel_name = str(row[col]).strip() if not pd.isna(row[col]) else None
                    
                    if not hotel_name:
                        continue
                    
                    
                    rooms_2 = int(row.get(f"rooms_2s_{col}",0))
                    rooms_3 = int(row.get(f"rooms_3s_{col}",0))
                    rooms_4 = int(row.get(f"rooms_4s_{col}",0))
                    
                    
                    hotel = db.query(Hotel).filter(Hotel.name == hotel_name).one_or_none()
                    if not hotel:
                        hotel = Hotel(name = hotel_name)
                        db.add(hotel)
                        db.commit()
                        db.refresh(hotel)
                    
                    
                    
                    create_rooms(
                        db=db,
                        guide_id=guide.id,
                        hotel_id=hotel.id,
                        hotel_name=hotel_name,
                        new_rooms={
                            2:rooms_2,
                            3:rooms_3,
                            4:rooms_4
                        }
                    )
                continue
            elif guide.hash_row != hash_row:
                if guide.name != guide_name:
                    update_guide(db=db ,guide=guide, guide_name=guide_name)

                for col in get_hotels_columns(df=df):
                    hotel_name = str(row[col]).strip() if not pd.isna(row[col]) else None

                    if not hotel_name:
                        continue

                    rooms_2 = int(row.get(f"rooms_2s_{col}",0))
                    rooms_3 = int(row.get(f"rooms_3s_{col}",0))
                    rooms_4 = int(row.get(f"rooms_4s_{col}",0))
                    
                    
                    hotel = db.query(Hotel).filter(Hotel.name == hotel_name).one_or_none()
                    if not hotel:
                        hotel = Hotel(name = hotel_name)
                        db.add(hotel)
                        db.commit()
                        db.refresh(hotel)
                    

                    update_rooms(
                        db=db,
                        guide_id=guide.id,
                        hotel_id=hotel.id,
                        hotel_name=hotel_name,
                        new_rooms={
                            2:rooms_2,
                            3:rooms_3,
                            4:rooms_4
                        },
                        warnings = warnings,
                        index = index
                    )
                
                
            



             
        except IntegrityError as ie:
            db.rollback()
            errors.append(f"Row {index}: {ie}")
        
        except Exception as e :
            db.rollback()
            errors.append(f"Row {index}: {e}")
        
    num_inserted = df.shape[0] - len(errors)
    return {
        "Inserted": num_inserted,
        "Warnings": warnings,
        "Failed": len(errors),
        "Errors": errors
    }


