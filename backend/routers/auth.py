from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta
from core.sequrity import authenticate_user , create_access_token , get_current_user
from schemas.user import Token , GuideUPload , GuideDB
from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm



auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/login" , response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm , Depends()] , db:Session = Depends(get_db)):
    user = authenticate_user(form_data.username , form_data.password , db)
    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username, "role": user.role.value})
    

    return Token(access_token=access_token , token_type="Bearer")
    