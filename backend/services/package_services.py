from fastapi import UploadFile , HTTPException , status
from sqlalchemy.orm import Session
import pandas as pd 
from schemas.package import PackageCreate , PackageRead
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from io import BytesIO
from datetime import date , datetime
from models.package import Package
from models.room import Room

def to_date(value):
    if pd.isna(value):
        return None
    if isinstance(value,str):
        return datetime.strptime(value,"%d/%m/%Y").date()
    if isinstance(value, datetime):
        return value.date()
    
    return None


async def process_package_file(file:UploadFile , db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []

    for index , row in df.iterrows():
        package_number = str(row["Package Number"]).strip()
        hotel1 = str(row["Hotel1"]).strip()
        check_in_date_h1 = to_date(row["Check-in date H1"])
        check_out_date_h1 = to_date(row["Check-out date H1"])
        rooms_2s_h1 = int(row["rooms_2s_h1"])
        rooms_3s_h1 = int(row["rooms_3s_h1"])
        rooms_4s_h1 = int(row["rooms_4s_h1"])

        hotel2 = str(row["Hotel2"]).strip()
        check_in_date_h2 = to_date(row["Check-in date H2"])
        check_out_date_h2 = to_date(row["Check-out date H2"])
        rooms_2s_h2 = int(row["rooms_2s_h2"])
        rooms_3s_h2 = int(row["rooms_3s_h2"])
        rooms_4s_h2 = int(row["rooms_4s_h2"])
        data={}
        
        
        if not pd.isna(row["Hotel3"]) :
            hotel3 = str(row["Hotel3"]).strip()
            check_in_date_h3 = to_date(row["Check-in date H3"])
            check_out_date_h3 = to_date(row["Check-out date H3"])
            rooms_2s_h3 = int(row["rooms_2s_h3"]) 
            rooms_3s_h3 = int(row["rooms_3s_h3"]) 
            rooms_4s_h3 = int(row["rooms_4s_h3"])

            data = {
            "package_number":package_number,
            "hotel1": hotel1,
            "check_in_date_h1":check_in_date_h1,
            "check_out_date_h1":check_out_date_h1,
            "rooms_2s_h1":rooms_2s_h1,
            "rooms_3s_h1":rooms_3s_h1,
            "rooms_4s_h1":rooms_4s_h1,

            "hotel2": hotel2,
            "check_in_date_h2":check_in_date_h2,
            "check_out_date_h2":check_out_date_h2,
            "rooms_2s_h2":rooms_2s_h2,
            "rooms_3s_h2":rooms_3s_h2,
            "rooms_4s_h2":rooms_4s_h2,

            "hotel3":hotel3,
            "check_in_date_h3":check_in_date_h3,
            "check_out_date_h3":check_out_date_h3,
            "rooms_2s_h3":rooms_2s_h3,
            "rooms_3s_h3":rooms_3s_h3,
            "rooms_4s_h3":rooms_4s_h3,
            }
        else:
            data = {
            "package_number":package_number,
            "hotel1": hotel1,
            "check_in_date_h1":check_in_date_h1,
            "check_out_date_h1":check_out_date_h1,
            "rooms_2s_h1":rooms_2s_h1,
            "rooms_3s_h1":rooms_3s_h1,
            "rooms_4s_h1":rooms_4s_h1,

            "hotel2": hotel2,
            "check_in_date_h2":check_in_date_h2,
            "check_out_date_h2":check_out_date_h2,
            "rooms_2s_h2":rooms_2s_h2,
            "rooms_3s_h2":rooms_3s_h2,
            "rooms_4s_h2":rooms_4s_h2,
            }
        
        

        try:
            package = PackageCreate(**data)
            create_package(db=db , package_data=package)

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

def create_package(db:Session, package_data:PackageCreate):
    check_package = db.query(Package).filter(Package.package_number == package_data.package_number).first()
    if check_package:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Package allready added")
    
    package = Package(**package_data.model_dump())
    db.add(package)
    db.commit()
    db.refresh(package)

    def create_rooms(hotel_name, rooms_2, rooms_3, rooms_4):
        room_list = []
        room_counter = 1
        for _ in range(rooms_2):
            room_list.append(Room(
                package_id = package.id , 
                hotel_name = hotel_name,
                capacity = 2,
                room_number=f"{hotel_name}-{room_counter}"
            ))
            room_counter +=1

        for _ in range(rooms_3):
            room_list.append(Room(
                package_id = package.id , 
                hotel_name = hotel_name,
                capacity = 3,
                room_number=f"{hotel_name}-{room_counter}"
            ))
            room_counter +=1
        
        for _ in range(rooms_4):
            room_list.append(Room(
                package_id = package.id , 
                hotel_name = hotel_name,
                capacity = 4,
                room_number=f"{hotel_name}-{room_counter}"
            ))
            room_counter +=1
        return room_list
    
    rooms = []
    rooms +=create_rooms(package.hotel1, package.rooms_2s_h1, package.rooms_3s_h1, package.rooms_4s_h1)
    rooms +=create_rooms(package.hotel2, package.rooms_2s_h2, package.rooms_3s_h2, package.rooms_4s_h2)
    if package.hotel3:
        rooms +=create_rooms(package.hotel3, package.rooms_2s_h3, package.rooms_3s_h3 , package.rooms_4s_h3)
    
    db.add_all(rooms)
    db.commit()
    

    return PackageRead.model_validate(package)


def delete_package(db:Session , package_number :int):
    package = db.query(Package).filter(Package.package_number == package_number).first()
    if package:
        db.delete(package)
        db.commit()
    else:
        raise HTTPException()
    