from typing import Any, Union
from sqlalchemy.orm import Session  
from .models import (Users)
from .schemas import UserSchema
from datetime import datetime , timezone , timedelta
import jwt
from src.connections import global_db
from passlib.context import CryptContext
SECRET_KEY = global_db._get_secret("kaewja","secret_kay",1)
REFRESH_KEY = global_db._get_secret("kaewja","refresh_key",1)
ALGORITHM = global_db._get_secret("kaewja","algorithm",1)
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 Minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 Days
password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_users(db:Session):
    return db.query(Users).all()
       
def get_user_by_id(db:Session, user_id:int):
    return db.query(Users).filter(Users.user_id == user_id).first()

def create_user(db:Session, user:UserSchema,):
    _user = Users(username=user.username, password=user.password, role=user.role, email=user.email, start_register=user.start_register)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user
    
def update_password(db:Session, user_id:UserSchema, pw: str):
    _user = db.query(Users).filter(Users.user_id == user_id).first()
    _user.password = pw
    db.commit()
    db.refresh()
    return _user
        
def delete_user(db:Session, user_id):
    _user = get_user_by_id(db=db, user_id=user_id)
    db.delete(_user)
    db.commit()
    
    
# // JWT
def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None):
    expires_delta = timedelta(minutes=expires_delta)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else : 
        expire = datetime.now(timezone.utc) + timedelta(minute=15)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt   

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, ALGORITHM)
    return encoded_jwt

def verify_password(plain_password,hashed_password):
    return password_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return password_context.hash(password)
    
def update_user(db:Session, user_info: schemas.UserInfo):
    _user_info = get_user_by_id(db=db, user_id=user_info.student_info_id)
    _user_info.firstname = user_info.firstname
    _user_info.lastname = user_info.lastname
    _user_info.phone = user_info.phone
    _user_info.major = user_info.major
    _user_info.year = user_info.year
    _user_info.password = get_password_hash(user_info.password)
    
    db.commit()
    db.refresh(_user_info)
    return _user_info