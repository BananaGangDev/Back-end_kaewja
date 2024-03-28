# 1st ORM
from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, SmallInteger, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from src.connections import global_db

Base = global_db.get_base()

#สร้างแล้ว
class Users(Base):
    
    __tablename__ = "users"
    
    user_id = Column(SmallInteger, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(SmallInteger, ForeignKey("role.role_id"), nullable=False)
    email = Column(String(200), nullable=True, unique=True)
    start_register = Column(Date, nullable=False)
    end_register = Column(Date, nullable=True)
    
    # user_info = relationship("UserInfo", back_populates="user")
    user_role = relationship("Role", back_populates="role")

# สร้างแล้ว
# class UserInfo(Base):
    
#     __tablename__ = "user_info"
    
#     user_info_id = Column(SmallInteger, primary_key=True)
#     firstname = Column(String(100), nullable=False)
#     lastname = Column(String(100), nullable=False)
#     email = Column(String(200), nullable=True, unique=True)
#     start_register = Column(Date, nullable=False)
#     end_register = Column(Date, nullable=True)
    
#     user = relationship("Users", back_populates="user_info")  

#สร้างแล้ว     
class Role(Base):
    __tablename__ = "role"
    
    role_id = Column(SmallInteger, primary_key=True)
    role_name = Column(String(100), nullable=False)
    role_description = Column(String(255), nullable=True)
    
    role = relationship("Users", back_populates="user_role")
    
#// JWT 
class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(BigInteger)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now())