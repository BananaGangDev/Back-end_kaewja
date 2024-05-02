from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import List

from .models import (Tagset, LabelTagset, LabelInfo)
from .schemas import (TagsetSchema, LabelSchema, TagsetSchemaCreate \
                    , TagsetSchemaPut, LabelSchemaCreate, LabelInfoSchema, LabelSchemaPut)

from datetime import datetime

#// Tagset
def get_tagsets(db:Session) -> List[TagsetSchema]:
    data = db.query(Tagset).order_by(Tagset.tagset_id).all()
    if data not in [None, []]:
        return [TagsetSchema.from_orm(i) for i in data]
    else:
        return []

def get_tagset_by_id(db:Session, tagset:int):
    data = db.query(Tagset).filter(Tagset.tagset_id == tagset).first()
    if data in [None, []]:
        return False
    else:
        return TagsetSchema.from_orm(data)


def create_tagset(db:Session , request: TagsetSchemaCreate) -> TagsetSchema:
    created_date = datetime.strptime(request.created_date,"%Y-%m-%d")
    tg = Tagset(tagset_name=request.tagset_name, created_date=created_date, created_by=request.created_by, marked=False, description=request.description)
    db.add(tg)
    db.commit()
    db.refresh(tg)
    return tg
    
    
def edit_tagset(req: TagsetSchemaPut,db:Session):
    tg = db.query(Tagset).where(Tagset.tagset_id == req.tagset_id).first()
    
    if tg in [[], None]:
        return False
    else:
        tg.tagset_name = req.tagset_name
        db.flush()
        tg.tagset_description = req.description
        db.commit()
        db.refresh(tg)
        return tg
    
def mark_tagset(tagset_id:int,db:Session):
    tg = db.query(Tagset).where(Tagset.tagset_id == tagset_id).first()
    
    if tg in [None, []]:
        return False
    else:
        if tg.marked == False:
            tg.marked = True
        else:
            tg.marked = False
        db.commit()
        return TagsetSchema.from_orm(tg)

def delete_tagset(db:Session, tagset_name:str, tagset_id:int):
    tg = db.query(Tagset).filter(Tagset.tagset_name == tagset_name).first()
    
    if tg in [None, []]:
        return False, "tagset"
    
    else:
        #// Check the tagset is empty?
        has_label = delete_label_by_tagset(db=db, tagset_id=tagset_id)
 
        if has_label == False:
            db.delete(tg)
            db.commit()
            return True, "tagset"
        else:
            db.delete(tg)
            db.commit()
            return True, "tagset and label"
        
    
#// Label
def create_label(req: LabelSchemaCreate, db:Session):
    date_info = datetime.strptime(req.created_date, "%Y-%m-%d")
    label_info = LabelInfo(label_description=req.label_description, created_by=req.created_by, created_date=date_info)
    
    label = LabelTagset(label_name=req.label_name, label_level=req.label_level, label_parent=req.label_parent, created_in_tagset=req.created_in_tagset)
    
    db.add(label_info)    
    db.flush()

    db.add(label)
    db.commit()
    return LabelSchema.from_orm(label), LabelInfoSchema.from_orm(label_info)
    
def get_label_in_tagset(tagset:int, db:Session):
    
    if get_tagset_by_id(tagset=tagset, db=db) == False:
        return False, "tagset"
    else:
        sql_command = select( 
                        LabelTagset.label_id, LabelTagset.label_name, LabelTagset.label_level,  \
                        LabelTagset.label_parent, LabelTagset.created_in_tagset, LabelInfo.label_description) \
                        .select_from(LabelTagset) \
                        .join(LabelInfo, and_(LabelTagset.label_id == LabelInfo.label_info_id, LabelTagset.created_in_tagset == tagset))
        result = db.execute(sql_command).fetchall()
    
        if result in [None, []]:
            return False, "label"
        else:
            result_list = [LabelSchema.from_orm(row) for row in result]
            return result_list, "_"

def delete_label_by_id(label_id:int, db:Session):
    label = db.query(LabelTagset).filter(LabelTagset.label_id == label_id).first()
    label_info = db.query(LabelInfo).filter(LabelInfo.label_info_id == label_id).first()
    
    if label in [None, []] or label_info in [None, []]:
        return False
    else:
        db.delete(label)
        db.flush()
        db.delete(label_info)
        db.commit()
        
        return True

def delete_label_by_tagset(tagset_id:str, db:Session):

    labels = db.query(LabelTagset).where(LabelTagset.created_in_tagset == tagset_id).all()
    label_ids = [label.label_id for label in labels]
    label_infos = db.query(LabelInfo).where(LabelInfo.label_info_id.in_(label_ids)).all()

    if labels in [None, []] and label_infos in [None, []]:
        return False
    
    else:
        for label in labels:
            db.delete(label)
        db.flush()    
        for label_info in label_infos:
            db.delete(label_info)
        db.commit()
        return True

def update_label_by_id(req:LabelSchemaPut, db:Session):
    label = db.query(LabelTagset).where(LabelTagset.label_id == req.label_id).first()
    label_info = db.query(LabelInfo).where(LabelInfo.label_info_id == req.label_id).first()
    if label in [None, []] or label_info in [None, []]:
        return False, "_"
    else:
        label.label_level = req.label_level
        label.label_name = req.label_name
        label.label_parent = req.label_parent
        db.flush()
        label_info.label_description = req.label_description
        db.commit()
        
        return LabelSchema.from_orm(label), LabelInfoSchema.from_orm(label_info)


#// LabelInfo
# TODO: Get -> get the label info
def get_label_info_by_id(db:Session, label_id: int):
    return db.query(LabelInfo).filter(LabelInfo.label_info_id == label_id).first()

