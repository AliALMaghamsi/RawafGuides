from jose import JWTError , jwt 
from typing import Annotated
from fastapi import status
from datetime import datetime , timedelta , timezone
from .config import settings
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db
from schemas.user import TokenData
from services.utils import get_user_by_id , get_user_by_username
from models.user import User , Role

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto" )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(hashed_password:str , plain_password:str):
    return pwd_context.verify(hashed_password , plain_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)


def create_access_token(data:dict , expires_delta : timedelta|None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode , settings.SECRET_KEY , settings.ALGORITHM)
    return encoded_jwt


def authenticate_user(username:str , password:str , db:Session = Depends(get_db) ):
    user = get_user_by_username(db , username)
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    
    return user



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)] , db:Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        
        id:int = int(payload.get("sub"))
        role: str = payload.get("role")
        username:str = payload.get("username")
        if username is None or id is None or role is None:
            raise credentials_exception
        token_data = TokenData(username=username , role=role , id=id)
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(db=db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user:User = Depends(get_current_user)):
    return current_user

async def get_current_admin_user(current_user:User = Depends(get_current_user)):
    if current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="only admin can access",

        )
    return current_user