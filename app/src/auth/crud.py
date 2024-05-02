from typing import Any, Union
from sqlalchemy.orm import Session  
from .models import Users,TokenTable
from .schemas import UserSchema,CreateNewUser,TokenSchema
from datetime import datetime , timezone , timedelta
import jwt
from src.connections import global_db
from passlib.context import CryptContext

SECRET_KEY = global_db._get_secret("engaged-arcanum-412912","secret_key",1)
REFRESH_KEY = global_db._get_secret("engaged-arcanum-412912","refresh_key",1)
ALGORITHM = global_db._get_secret("engaged-arcanum-412912","algorithm",2)
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 Minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 Days
password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_users(db:Session):
    return db.query(Users).all()
       
def get_user_by_username(db:Session, username:str):
    return db.query(Users).filter(Users.username == username).first()

def create_user(db:Session, user:CreateNewUser):
    _user = Users(user_id=1000+(db.query(Users).count()+1),username=user.username, password=get_password_hash(user.password),firstname=user.firstname,lastname=user.lastname, role=user.role, email=user.email, start_register=datetime.now().date()
        )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user
        
def delete_user(db:Session, username):
    _user = get_user_by_username(db=db, username=username)
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
    verify = password_context.verify(plain_password,hashed_password)
    print(verify)
    print(plain_password)
    print(hashed_password)
    return verify

def get_password_hash(password):
    hashed_password = password_context.hash(password)
    # print(password)
    # print(hashed_password)
    return hashed_password
    
def update_user(db:Session, user_info: UserSchema):
    _user_info = db.query(Users).filter(Users.user_id == user_info.user_id).first()
    _user_info.user_id = user_info.user_id
    _user_info.username = user_info.username
    _user_info.password = user_info.password
    _user_info.firstname = user_info.firstname
    _user_info.lastname = user_info.lastname
    _user_info.role = user_info.role
    _user_info.email = user_info.email
    _user_info.start_register = user_info.start_register
    _user_info.end_register = user_info.end_register
    
    db.commit()
    db.refresh(_user_info)
    return _user_info

def update_status_token(db:Session, access_token):
    _token = db.query(TokenTable).filter(TokenTable.access_token==access_token).first()
    _token.status = False
    db.commit()
    db.refresh(_token)
    return _token