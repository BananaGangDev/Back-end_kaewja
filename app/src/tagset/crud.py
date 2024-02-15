from sqlalchemy.orm import Session
from .models import (Tagset, LabelTagset, LabelInfo)
from .crud import (TagsetSchema)
from src.connections import global_db

#// Tagset
# TODO: GET -> get all tagsets
def get_tagsets(db:Session):
    return db.query(Tagset).all()

def get_tagset_by_id(db:Session, tagset_id:int):
    return db.query(Tagset).filter(TagsetSchema.tagset_id == tagset_id).first()

#TODO: POST -> create new tagset
def create_tagset(db:Session ,tagset: TagsetSchema):
    _tg = Tagset(tagset_name=tagset.tagset_name,
                 created_date=tagset.created_date,
                 created_by=tagset.created_by)
    db.add(_tg)
    db.commit()
    db.refresh()
    return _tg

#TODO: PUT -> edit existing tagset (name, description)
def edit_tagset(db:Session,tagset_id:int, text:str, part:bool = True ):
    _tg = get_tagset_by_id(db, tagset_id)
    
    if part == True:
        _tg.description = text
    else:
        _tg.name = text
    
    db.commit()
    db.refresh()
    return _tg
    

#TODO: DELETE -> delete existing tagset
def delete_tagset(db:Session, tagset_id:int):
    _tg = get_tagset_by_id(db, tagset_id)
    db.delete(_tg)
    db.commit()
    
    
#// Label

# TODO: POST -> Create label
def create_label():
    pass

# TODO: GET ->  get all labeld

# TODO: DELETE -> delete the label

# TODO: PUT -> Edit the label (Tag, description)