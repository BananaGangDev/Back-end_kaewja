# 2nd ORM
from pydantic import BaseModel, Field, PositiveInt
from typing import List, Optional
from datetime import date


class TagsetSchema(BaseModel):
    tagset_id: PositiveInt
    tagset_name: str = Field(..., max_length=100)
    created_date: date
    created_by: PositiveInt
    class Config:
        orm_mode = True

class LabelSchema(BaseModel):
    label_id:PositiveInt
    label_name:str = Field(..., max_length=100)
    label_level: PositiveInt
    label_parent: str = Field(..., max_length=100)
    created_in_tagset: PositiveInt
    class Config:
        orm_mode = True

class LabelInfoSchema(BaseModel):
    label_info_id: PositiveInt
    label_description: str = Field(..., max_length=255)
    created_by: PositiveInt
    created_date: date
    class Config:
        orm_mode = True