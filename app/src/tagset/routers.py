# Web
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.orm import Session


# data
from .schemas import (TagsetSchema, TagsetSchemaCreate, LabelSchema \
                    , TagsetSchemaPut, LabelSchemaCreate, LabelSchemaPut)
from .crud import (get_tagsets, get_label_in_tagset \
                    , create_tagset, get_tagset_by_id \
                    , edit_tagset, delete_tagset, create_label \
                    , delete_label_by_id, update_label_by_id, mark_tagset)

from src.connections import global_db
from typing import List

# Validation
from .exceptions import (check_name, validate_format_datetime, check_tagset_existing)

router = APIRouter(
    prefix="/tagsets",
    tags=["Tagset"]
)
def get_db():
    db = global_db.get_sessionlocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/all', status_code=200, response_model=List[TagsetSchema])
async def tagsets(db:db_dependency):
    all_tagsets = get_tagsets(db)
    return all_tagsets

@router.get('/', status_code=200, response_model=TagsetSchema)
async def tagset_by_id(tagset_id:int, db:db_dependency):
    find_tg = get_tagset_by_id(tagset=tagset_id, db=db)
    if not (find_tg):
        raise HTTPException(status_code=400, detail=f"Not found tagset number {tagset_id}")
    else:
        return find_tg

@router.get('/labels', status_code=200, response_model=List[LabelSchema])
async def labels(tagset_id:int,db:db_dependency):
    data, not_found = get_label_in_tagset(db=db, tagset=tagset_id)
    if data == False and not_found == "tagset":
        raise HTTPException(status_code=400, detail=f"Not found tagset {tagset_id}")
    elif data == False and not_found == "label":
        raise HTTPException(status_code=400, detail=f"This tagset id {tagset_id} doesn't have a label")
    else:
        return data

@router.post('/create', status_code=201, response_model=TagsetSchema)
async def tagsets_POST(request: TagsetSchemaCreate,db:db_dependency):
    
    if check_name(request.tagset_name):
        if validate_format_datetime([request.created_date],r"\d{4}-\d{2}-\d{1,2}"):
            n_tg = create_tagset(db, request)
            return n_tg
        else:
            raise HTTPException(status_code=400, detail="Wrong date format")
    else:
        raise HTTPException(status_code=400, detail="Tagset name doesn't allow a special character and number")


@router.post('/labels/create', status_code=201)
async def new_label(request:LabelSchemaCreate, db:db_dependency):
    
    if check_name(request.label_name):    
        label, label_info = create_label(req=request, db=db)
        return label, label_info   
    else:
        raise HTTPException(status_code=400, detail="Label name doesn't allow a special character and number")

@router.put('/bookmark', status_code=200)
async def bookmark(tagset_id:int, db:db_dependency):
    data = mark_tagset(tagset_id=tagset_id,db=db)
    if data == False:
        raise HTTPException(status_code=400, detail=f"Not found tagset id {tagset_id}")
    else:
        return data
    
@router.put("/update", status_code=200, response_model=TagsetSchema)
async def tagsets_PUT(request: TagsetSchemaPut,db:db_dependency):
    update_finish = edit_tagset(db=db, req=request)
    
    if update_finish == False:
        raise HTTPException(status_code=400, detail=f"Not found, tagset id {request.tagset_id}")
    else:
        return update_finish


@router.put('/labels/update', status_code=200)
async def update_label(request:LabelSchemaPut, db:db_dependency):
    label, label_info = update_label_by_id(req=request, db=db)
    
    if label == False:
        raise HTTPException(status_code=400, detail=f"Not found label id {request.label_id}")
    else:
        return label, label_info
    
@router.delete('/delete')
async def tagsets_DELETE(tagset_name:str,tagset_id:int, db:db_dependency):
    
    
    if check_tagset_existing(tagset_id=tagset_id, tagset_name=tagset_name, db=db):
        delete_finish, item = delete_tagset(db=db, tagset_name=tagset_name, tagset_id=tagset_id)
        
        if delete_finish and item == "tagset and label":
            return {"detail": "Delete both tagset and label beneath successfully"}
        elif delete_finish and item == "tagset":
            return {"detail": "Delete tagset successfully"}
        elif delete_finish == False and item == "tagset":
            raise HTTPException(status_code=400, detail=f"Not found tagset id {tagset_name}")
    else:
        raise HTTPException(status_code=400, detail=f"Name tagset or Id tagset may be wrong")

@router.delete('/labels/delete')
async def label_DELETE(label_id:int, db:db_dependency):
    label = delete_label_by_id(label_id=label_id, db=db)
    
    if label == False:
        raise HTTPException(status_code=400,detail=f"Not found, label id {label_id}")
    else:
        return {"detail": f"Delete label id {label_id} successfully"}

    




