from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from src.dashboard.models import Dashboard
from src.dashboard.schemas import CreateStat
from src.connections import global_db
from sqlalchemy.orm import Session  
from src.tagset.models import LabelTagset,LabelInfo
from src.tagset.schemas import LabelSchema

def get_label_by_label_id(db:Session,label_id):
    return db.query(LabelTagset).filter(LabelTagset.label_id==label_id).first()

def get_label_by_label_name(db:Session,label_name):
    return db.query(LabelTagset).filter(LabelTagset.label_name==label_name).first()

def check_label_by_label_name(db:Session,label_name,tagset_id):
    return db.query(LabelTagset).filter(LabelTagset.label_name==label_name,LabelTagset.created_in_tagset==int(tagset_id)).first()

def add_data(db:Session,filename,tagset_id,label_id,count):
    _data = Dashboard(id=1000+(db.query(Dashboard).count()+1),filename=filename,tagset_id=int(tagset_id),label_id=int(label_id),count=int(count))
    db.add(_data)
    db.commit()
    db.refresh(_data)
    return _data

def check_label_by_file(db:Session,filename,label_id):
    return db.query(Dashboard).filter(Dashboard.filename==filename,Dashboard.label_id==int(label_id)).first()

def update_data(db:Session,filename,label_id,new_count):
    _data = db.query(Dashboard).filter(Dashboard.filename==filename,Dashboard.label_id==label_id).first()
    _data.count = new_count
    
    db.commit()
    db.refresh(_data)
    return _data

def get_stat_by_id(db:Session,tagset_id):
    return db.query(Dashboard).filter(Dashboard.tagset_id==int(tagset_id)).all()
    
def get_document_by_tagset_id(db:Session,tagset_id):
    # return db.query(Dashboard.filename,func.count(Dashboard.filename)).group_by(Dashboard.filename).all()
    data = db.query(Dashboard).filter(Dashboard.tagset_id==str(tagset_id)).all()
    if data in [None,[]]:
        return False
    else :
        return data

def get_root_label(db:Session,tagset_id):
    data = db.query(LabelTagset).filter(LabelTagset.created_in_tagset==int(tagset_id),LabelTagset.label_parent=="ROOT").all()
    if data in [None,[]]:
        return False
    else :
        return data

def get_label_by_root(db:Session,tagset_id,label_parent,label_level):
    data = db.query(LabelTagset).filter(LabelTagset.created_in_tagset==int(tagset_id),LabelTagset.label_level==int(label_level),LabelTagset.label_parent==label_parent).all()
    if data in [None,[]]:
        return False
    else :
        return data

def get_label_description(db:Session,label_name):
    _label = get_label_by_label_name(db=db,label_name=label_name)
    _label_info = db.query(LabelInfo).filter(LabelInfo.label_info_id==_label.label_id).first()
    return _label_info.label_description