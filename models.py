from venv import create
from sqlalchemy import Column, Integer, String, Boolean, text, true
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class Post(Base):
    __tablename__ = "posts" 
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    create_at = Column(TIMESTAMP(timezone=true), nullable=False, server_default= text('now()'))  
    

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=true), nullable=False, server_default= text('now()')) 