    # 2nd ORM
from pydantic import BaseModel, Field, conint
from typing import List, Optional
from datetime import date


class TagsetSchema(BaseModel):
    tagset_id: int = Field(primary_key=True)
    tagset_name: str = Field(..., max_length=100)
    created_date: date
    created_by: int
    marked:bool = Field(default=False)
    description: Optional[str] = Field(default=None, max_length=500)
    
    class Config:
        from_attributes=True

class LabelSchema(BaseModel):
    label_id: Optional[int] = Field(primary_key=True)
    label_name:str = Field(..., max_length=100)
    label_level: int
    label_parent: str = Field(..., max_length=100)
    created_in_tagset: int
    label_description: Optional[str] = Field(default=None, max_length=500)
    class Config:
        from_attributes=True

class LabelInfoSchema(BaseModel):
    label_info_id:int
    label_description: Optional[str] = Field(default=None,max_length=255)
    created_by: int
    created_date: date

    class Config:
        from_attributes=True



class LabelSchemaCreate(BaseModel):
    # Label
    label_name:str = Field(max_length=100)
    label_level: int
    label_parent: Optional[str] = Field(default="ROOT",max_length=100)
    created_in_tagset: int
    
    # Label info
    label_description: Optional[str] = Field(default=None, max_length=255)
    created_by: int
    created_date: str
    
    class Config:
        from_attributes=True

class LabelSchemaPut(BaseModel):
    # Label
    label_id:int
    label_name:str = Field(..., max_length=100)
    label_level: int
    label_parent: str = Field(..., max_length=100)
    # Label info
    label_description: str = Field(..., max_length=255)
    
    class Config:
        from_attributes=True


class TagsetSchemaCreate(BaseModel):
    
    tagset_name: str = Field(..., max_length=100)
    created_date: str
    created_by: int
    description: Optional[str] = Field(default=None, max_length=500)
    
    class Config:
        from_attributes=True
        
class TagsetSchemaPut(BaseModel):
    tagset_id: int
    tagset_name: str = Field(..., max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    
    class Config:
        from_attribute = True
    