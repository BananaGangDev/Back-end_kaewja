from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# data
#from .crud import (get_tagsets)
from src.connections import global_db

router = APIRouter(
    prefix="/tagset",
    tags=["Tagset"]
)
def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
    finally:
        db.close()


# @router.get('/')
# def tagset_page(db:Session=Depends(get_db)):
#     all_tagsets = get_tagsets(db)
    
#     return {'data': all_tagsets}