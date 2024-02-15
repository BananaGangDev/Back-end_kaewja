from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Jwt
from datetime import timedelta, datetime
from typing import Annotated
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


# Data
from .crud import (get_users_by_id)
from src.connections import global_db
from .models import Users

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#// Make sure the database is closed even if it fail or not
def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
        
    finally:
        db.close()
# db_dependency = Annotated[Session]

SECRET_KEY = ""
ALGORITHM = "H5256"



@router.get("/")
def index(db: Session=Depends(get_db)):
    users = get_users_by_id(db,1)
    return {"data": users}


#// JWT
@router.post("/token")
def login_for_access_token(self):
    pass