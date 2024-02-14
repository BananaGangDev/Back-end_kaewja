# 1st ORM
from sqlalchemy import Column, String, SmallInteger, Date, ForeignKey
from sqlalchemy.orm import relationship
from connections import global_db

Base = global_db.get_base()

class Tagset(Base):
    __tablename__ = "tagset"
    
    tagset_id = Column(SmallInteger, primary_key=True)
    tagset_name = Column(String(100), nullable=False)
    created_date = Column(Date, nullable=False)
    created_by = Column(SmallInteger, nullable=False)

class LabelTagset(Base):
    __tablename__ = "label_tagset"

    label_id = Column(SmallInteger, ForeignKey("label_info.label_info_id", primary_key=True))
    label_name = Column(String(100), nullable=False)
    label_level = Column(SmallInteger, nullable=False)
    label_parent = Column(String(100), nullable=False)
    created_in_tagset = Column(SmallInteger, nullable=False)
    
    label_info = relationship("LabelInfo", back_populates="label_tagset")

class LabelInfo(Base):
    __tablename__ = "label_info"
    
    label_info_id = Column(SmallInteger, primary_key=True)
    label_description = Column(String(255), nullable=True)
    created_by = Column(SmallInteger, nullable=False)
    created_date = Column(Date, nullable=False)
    
    label = relationship("LabelTagset",back_populates="label_info")