# 2nd ORM
from pydantic import BaseModel, Field, EmailStr, PositiveInt
from typing import List, Optional, Generic, TypeVar
from pydantic.generics import GenericModel
from datetime import datetime,date


class UserSchema(BaseModel):
    user_id: PositiveInt
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    firstname: str = Field(..., max_length=100)
    lastname: str = Field(..., max_length=100)
    role: PositiveInt
    email: Optional[EmailStr]
    start_register: date
    end_register: Optional[date]
    
    class Config:
        from_attributes=True
        
class CreateNewUser(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    firstname: str = Field(..., max_length=100)
    lastname: str = Field(..., max_length=100)
    role: PositiveInt
    email: Optional[EmailStr]
    
    class Config:
        orm_mode = True
        
class RoleSchema(BaseModel):
    role_id: PositiveInt
    # TODO: write the REGEX
    role_name: str = Field(..., pattern=r"")
    role_description: Optional[str]
        
    class Config:
        from_attributes=True

#// JWT
class requestdetails(BaseModel):
    username : str
    password: str
    
    class Config:
        orm_mode = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    class Config:
        orm_mode = True

class changepassword(BaseModel):
    user_id: int
    old_password: str
    new_password: str
    
    class Config:
        orm_mode = True

class TokenCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_date:datetime
    
    class Config:
        orm_mode = True
    
class TokenData(BaseModel):
    user_id: int | None = None
    
    class Config:
        orm_mode = True