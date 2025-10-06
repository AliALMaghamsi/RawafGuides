from fastapi import UploadFile
from sqlalchemy.orm import Session
import pandas as pd 
from schemas.package import PackageCreate
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from io import BytesIO
from datetime import date , datetime
from models.package import Package


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
        hotel2 = str(row["Hotel2"]).strip()
        check_in_date_h2 = to_date(row["Check-in date H2"])
        check_out_date_h2 = to_date(row["Check-out date H2"])
        hotel3 = str(row["Hotel3"]).strip()
        check_in_date_h3 = to_date(row["Check-in date H3"])
        check_out_date_h3 = to_date(row["Check-out date H3"])
        data = {
            "package_number":package_number,
            "hotel1": hotel1,
            "hotel2": hotel2,
            "hotel3":hotel3,
            "check_in_date_h1":check_in_date_h1,
            "check_out_date_h1":check_out_date_h1,
            "check_in_date_h2":check_in_date_h2,
            "check_out_date_h2":check_out_date_h2,
            "check_in_date_h3":check_in_date_h3,
            "check_out_date_h3":check_out_date_h3
            }
        

        try:
            package = PackageCreate(**data)
            create_package(db=db , package_data=package)

        except ValidationError as ve:
            errors.append(f"Row:{index}: {ve}")

        except IntegrityError as ie :
            db.rollback()
            errors.append(f"Row:{index}: {ve}")
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
        raise ValidationError("Package was added")
    
    package = Package(**package_data.model_dump())
    db.add(package)
    db.commit()
    db.refresh(package)
    return {"username": package.package_number,"id": package.id}

