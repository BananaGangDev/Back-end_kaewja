from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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
ALGORITHM = global_db._get_secret("kaewja","algorithm",1)
SECRET_KEY = global_db._get_secret("kaewja","secret_key",2)
REFRESH_SECRET_KEY = global_db._get_secret("kaewja","refresh_key",2)

#// Make sure the database is closed even if it fail or not
def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
        
    finally:
        db.close()


@router.get("/")
def index(db: Session=Depends(get_db)):
    users = crud.get_user_by_id(db,1)
    return {"data": users}

#login
@router.post("/login/",status_code=200)
async def log_in(login_item:schemas.requestdetails ,db:Session=Depends(get_db)):
    user = crud.get_user_by_id(db,user_id=login_item.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This ID doesn't have account. Please sign up.")
    
    if not crud.verify_password(login_item.password,crud.get_password_hash(login_item.password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is wrong.")
    
    access=crud.create_access_token(user.user_id,expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh = crud.create_refresh_token(user.user_id,expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES)

    token_db = TokenTable(user_id=user.user_id,  access_token=access,  refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }
    
#Sign up ห้ามแก้
@router.post("/create_new_user/", status_code=201) 
async def register_user(user: schemas.UserSchema,db: Session=Depends(get_db)):
    existing_user = db.query(Users).filter_by(student_info_id=user.user_id).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is already registered.")
    
    new_user = crud.create_user(user_info=user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"user created successfully"}

@router.get('/get_uavailable_token_user')
def get_users_log_in( dependencies=Depends(JWTBearer()),db: Session = Depends(get_db)):
    return db.query(TokenTable).filter_by(status=True).all()

@router.post('/change-password')
def change_password(request: schemas.changepassword, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user_id == request.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not crud.verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encrypted_password = crud.get_password_hash(request.new_password)
    user.password = encrypted_password
    db.commit()
    
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
    if info:
        db.delete(info)
        #existing_token = db.query(models.TokenTable).where(models.TokenTable.user_id==info.user_id).delete()
        db.commit()
        
    existing_token = db.query(TokenTable).filter(TokenTable.access_token==token).first()
    if existing_token:
        existing_token.status=False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message":"Logout Successfully"} 