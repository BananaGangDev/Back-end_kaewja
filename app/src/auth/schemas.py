# 2nd ORM
from pydantic import BaseModel, Field, EmailStr, PositiveInt
from typing import List, Optional, Generic, TypeVar
from pydantic.generics import GenericModel
from datetime import date

T = TypeVar("T")

class UserSchema(BaseModel):
    user_id: PositiveInt
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    role: PositiveInt
    
    class Config:
        orm_mode = True
    
    
class UserInfoSchema(BaseModel):
    user_info_id: PositiveInt
    firstname: str = Field(..., max_length=100)
    lastname: str = Field(..., max_length=100)
    email: Optional[EmailStr]
    start_register: date
    end_register: Optional[date]
    class Config:
        orm_mode = True
    
    
class RoleSchema(BaseModel):
    role_id: PositiveInt
    role_name: str = Field(..., pattern=r"")
    role_description: Optional[str]
    class Config:
        orm_mode = True
    
class Token(BaseModel):
    access_token: str
    token_type: str