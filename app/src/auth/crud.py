from sqlalchemy.orm import Session  
from .models import (Users)
from .schemas import UserSchema

def get_users(db:Session):
    return db.query(Users).all()
    
    
def get_users_by_id(db:Session, user_id:int):
    return db.query(Users).filter(Users.user_id == user_id).first()


def create_user(db:Session, user:UserSchema):
    _user = Users(username=user.username, password=user.password, role=user.role)
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
    _user = get_users_by_id(db=db, user_id=user_id)
    db.delete(_user)
    db.commit()
    
    
# // JWT
def create_access_token(self):
    pass
def autheticate_user(self):
    pass

    