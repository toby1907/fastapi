from venv import create
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, text, true
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class Post(Base):
    __tablename__ = "posts" 
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))  
    # Add foreign key to users table with cascade delete
    owner_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"),  # CASCADE delete when user is deleted
        nullable=False
    )
    
    # Relationship to User model (optional but useful for ORM operations)
    owner = relationship("User", back_populates="posts")
    

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()')) 
    # Relationship to posts (optional)
    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")
    
    
    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    