from models.user import User
from fastapi import UploadFile
from sqlalchemy.orm import Session
import pandas as pd 
from schemas.package import PackageCreate
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from io import BytesIO
from datetime import date


async def process_package_file(file:UploadFile , db:Session):
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    errors = []

    for index , row in df.iterrows():
        package_number = str(row["Package Number"]).strip()
        hotel1 = str(row["Hotel1"]).strip()
        check_in_date_h1 = date(row["Check-in date H1"])
        check_out_date_h1 = date(row["Check-out date H1"])
        hotel2 = str(row["Hotel2"]).strip()
        check_in_date_h2 = date(row["Check-in date H2"])
        check_out_date_h2 = date(row["Check-out date H2"])
        hotel3 = str(row["Hotel3"]).strip()
        check_in_date_h3 = date(row["Check-in date H3"])
        check_out_date_h3 = date(row["Check-out date H3"])
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
        package = PackageCreate(**data)

        try:
            pass

        except Exception as e :
            pass
      