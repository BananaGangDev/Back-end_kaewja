from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_ 
from src.dashboard import schemas
from src.connections import global_db
import re
from src.tagset.crud import get_tagset_by_id
from typing import Annotated

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/create_stat",status_code=200)
def create_stat(string,tagset_id,db:db_dependency):
        tagset = get_tagset_by_id(db=db,tagset=tagset_id)
        print(tagset)
        print(type(tagset))
        