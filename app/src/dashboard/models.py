from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, SmallInteger, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from src.connections import global_db

Base = global_db.get_base()

class Dashboard(Base):
    
    __tablename__ = "dashboard"
    
    id = Column(SmallInteger,primary_key=True)
    filename = Column(String(500),nullable=False)
    tagset_id = Column(SmallInteger,nullable=False)
    label_id = Column(SmallInteger,nullable=False)
    count = Column(SmallInteger,nullable=False)
    
