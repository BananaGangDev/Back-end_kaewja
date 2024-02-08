from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Jwt
from datetime import timedelta, datetime
from typing import Annotated


# Data
from .crud import (get_users_by_id)
from src.connections import global_db
#from .schemas import  Response

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
        
    finally:
        db.close()


SECRET_KEY = ""
ALGORITHM = "H5256"



@router.get("/")
def index(db: Session=Depends(get_db)):
    users = get_users_by_id(db,1)
    return {"data": users}

