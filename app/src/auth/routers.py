from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_ 

# Jwt
from datetime import timedelta, datetime, timezone
from typing import Annotated
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


# Data
from src.auth import crud,schemas
from src.auth.models import Users,TokenTable,Role
from src.connections import global_db
from src.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 Minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 Days
ALGORITHM = global_db._get_secret("engaged-arcanum-412912","algorithm",2)
SECRET_KEY = global_db._get_secret("engaged-arcanum-412912","secret_key",1)
REFRESH_SECRET_KEY = global_db._get_secret("engaged-arcanum-412912","refresh_key",1)

#// Make sure the database is closed even if it fail or not
def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
        
    finally:
        db.close()


@router.get("/")
def index(db: Session=Depends(get_db)):
    users = crud.get_users(db)
    return {"data": users}

#login
@router.post("/login/",status_code=200)
async def log_in(login_item:schemas.requestdetails ,db:Session=Depends(get_db)):
    user = crud.get_user_by_username(db,username=login_item.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This ID doesn't have account. Please sign up.")
    
    if not crud.verify_password(login_item.password,crud.get_password_hash(login_item.password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is wrong.")
    
    access=crud.create_access_token(user.username,expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh = crud.create_refresh_token(user.username,expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES)

    token_db = TokenTable(user_id=user.user_id,  access_token=access,  refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "user_id" : user.user_id,
        "access_token": access,
        "refresh_token": refresh,
    }
    
#Sign up ห้ามแก้
@router.post("/create-new-user/", status_code=201) 
async def register_user(user: schemas.CreateNewUser,db: Session=Depends(get_db)):
    if user.email:
        existing_user = db.query(Users).filter(or_(Users.username==user.username,Users.email==user.email,)).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID or Email is already registered.")
    
    new_user = crud.create_user(db=db,user=user)
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    return {"message":"user created successfully"}

@router.get('/get_available_token_user')
def get_users_log_in(db: Session = Depends(get_db)):
    return db.query(TokenTable).filter_by(status=True).all()

@router.post('/change-password')
def change_password(request: schemas.changepassword, db: Session = Depends(get_db),dependencies=Depends(JWTBearer())):
    user = db.query(Users).filter(Users.user_id == request.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not crud.verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encrypted_password = crud.get_password_hash(request.new_password)
    user.password = encrypted_password
    crud.update_user(db=db,user_info=user)
    return {"message": "Password changed successfully"}

@router.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    token=dependencies
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(TokenTable).all()
    info=[]
    for record in token_record :
        print("record",record)
        if (datetime.now(timezone.utc).replace(tzinfo=None) - record.created_date).days > 1:
            info.append(record.user_id)
        
    access_token = db.query(TokenTable).filter(TokenTable.access_token==token).first().access_token
    if access_token:
        existing_token = crud.update_status_token(db=db,access_token=access_token)
        if existing_token and existing_token.status == False:
            return {"message":"Logout Successfully"} 
        else : 
            return {"message":"Invalid Token"}