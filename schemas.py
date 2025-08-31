
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field, validator,field_validator



class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    create_at: datetime
    
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr  # This automatically validates email format
    password: str = Field(..., min_length=6)  # Requires min 6 characters
    
    # Optional: Custom validation example
    @field_validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        # Add more checks like uppercase, numbers, etc.
        return v
    
class UserCreateResponse(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime
    
    class Config:
        orm_mode = True

# You can add more schemas as needed, e.g., for user login, token response, etc.    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Union[int, str]


