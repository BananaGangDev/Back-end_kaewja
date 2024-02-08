# 1st ORM
from sqlalchemy import Column, String, SmallInteger, Date
from sqlalchemy.orm import relationship
from connections import global_db

Base = global_db.get_base()

class Tagset(Base):
    __tablename__ = "tagset"
    
    tagset_id = Column()
    tagset_name = Column()
    created_date = Column()
    created_by = Column()

class LabelTagset(Base):
    __tablename__ = "label_tagset"

    

class LabelInfo(Base):
    __tablename__ = "label_info"
    
    label_info_id = Column()
    label_description = Column()
    created_by = Column()
    created_date = Column()