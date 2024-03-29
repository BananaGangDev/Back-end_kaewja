# 2nd ORM
from pydantic import BaseModel, Field, EmailStr, PositiveInt
from typing import List, Optional, Generic, TypeVar
from datetime import date


class UserSchema(BaseModel):
    user_id: PositiveInt
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    role: PositiveInt
    
    class Config:
        from_attributes=True
        
class UserInfoSchema(BaseModel):
    user_info_id: PositiveInt
    firstname: str = Field(..., max_length=100)
    lastname: str = Field(..., max_length=100)
    email: Optional[EmailStr]
    start_register: date
    end_register: Optional[date]
        
    class Config:
        from_attributes=True
        
class RoleSchema(BaseModel):
    role_id: PositiveInt
    # TODO: write the REGEX
    role_name: str = Field(..., pattern=r"")
    role_description: Optional[str]
        
    class Config:
        from_attributes=True

#// JWT
class Token(BaseModel):
    access_token: str
    token_type: str
class UserRequest(BaseModel):
    pass