# 2nd ORM
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date




#// Imported document
class DocImportSchema(BaseModel):
    doc_import_id:int
    doc_import_name:str = Field(max_length=100)
    doc_import_path:str = Field(max_length=200)
    doc_import_status: Optional[bool] = Field(default=False)

class DocImportSchemaCreate(BaseModel):
    doc_import_name:str = Field(max_length=100)
    doc_import_path:str = Field(max_length=200)
    doc_import_status: Optional[bool] = Field(default=False)



#// Exported document
class DocExportSchema(BaseModel):
    doc_export_id: int
    doc_export_name: str = Field(max_length=100)
    export_by: int
    export_date: date
    
    
class DocExportSchemaCreate(BaseModel):
    doc_export_name: str = Field(max_length=100)
    export_by: int
    export_date: date
