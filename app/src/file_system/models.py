# 1st ORM
from sqlalchemy import Column, SmallInteger, Date, String, Integer, Boolean
from src.connections import global_db


Base = global_db.get_base()


#// Imported document

class DocImport(Base):
    __tablename__ = "doc_import"
    
    doc_import_id = Column(Integer, primary_key=True)
    doc_import_name = Column(String(100), nullable=False)
    doc_import_path = Column(String(200), nullable=False)
    doc_import_status = Column(Boolean, nullable=False, default=False)
    
    
    
class DocImportInfo(Base):
    __tablename__ = "doc_import_info"
    
    doc_import_info_id = Column(Integer, primary_key = True)
    imported_by = Column(SmallInteger, nullable=False)
    imported_date = Column(Date, nullable=False)
    
    

#// Exported document
class DocExport(Base):
    __tablename__ = "doc_export"
    doc_export_id = Column(Integer, primary=True)
    doc_export_name = Column(String(100), nullable=False)
    export_by = Column(SmallInteger, nullable=False)
    export_date = Column(Date, nullable=False)
    
    
