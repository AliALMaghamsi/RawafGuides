from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.orm import Session

from core.sequrity import get_current_active_user
from schemas.pilgrim import PilgrimCreate , PilgrimRead

guide_router = APIRouter(
    prefix="/guide",
    tags=["guide"],
)

