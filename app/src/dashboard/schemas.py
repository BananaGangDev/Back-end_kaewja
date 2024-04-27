
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class CreateStat(BaseModel):
    id:int
    filename:str = Field(max_length=500)
    tagset_id:int 
    label_id:int
    count:int
    class Config:
        from_attributes=True
    
