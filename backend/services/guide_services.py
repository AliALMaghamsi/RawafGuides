from models.user import User
from models.pilgrim import Pilgrim
from fastapi import UploadFile , HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd 
from schemas.user import GuideUPload , GuideRead
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from core.sequrity import get_password_hash
from io import BytesIO
from .utils import get_package_id_by_number
from models.package import Package


async def process_guide_file(file: UploadFile , db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []
    for index, row in df.iterrows():
        
        name = str(row["name"]).strip()
        passport_number = str(row["passport_number"]).strip()
        package_number = str(row["package_number"]).strip()

        row_dict = {"name": name, "passport": passport_number , "package_number":package_number}
        
        try:
            guide = GuideUPload(**row_dict)
            create_guide_user(db=db , guide_data=guide)
        
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


def create_guide_user(db: Session , guide_data:GuideUPload):
    passport_number = guide_data.passport
    name = guide_data.name
    package_id = get_package_id_by_number(db=db , package_number=guide_data.package_number)
    if not package_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Package with this number not found")
    
    check_user = db.query(User).filter(User.passport == passport_number).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user already added")
    

    username = name.replace(" ", "") + "_" + passport_number[:4]
    hashed_password = get_password_hash(passport_number)
    guide = User(
            name = name,
            passport = passport_number,
            username = username,
            hashed_password = hashed_password,
            package_id = package_id,
    )

    db.add(guide)
    db.commit()
    db.refresh(guide)
    
    return GuideRead.model_validate(guide)

    





