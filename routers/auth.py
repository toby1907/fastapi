from fastapi import APIRouter, Depends, status, HTTPException,Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
import models
from database import get_db 
from utils import verifyPassword
from schemas import UserLogin, Token 
from oauth2 import createAccessToken


router = APIRouter(prefix="/auth", tags=["Authentication"])  # ✅ Groups under "Authentication" in docs

@router.post("/login", 
    response_model=Token,
    summary="User login",
    description="Authenticate user and return JWT access token")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):  
    # 1. Find user by email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() 
     
    # 2. Check if user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # 3. Verify password (assuming verifyPassword is your function)
    if not verifyPassword(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # 4. Create JWT token
    access_token = createAccessToken(data={"user_id": user.id}) 
    
    # 5. Return token (response_model=Token ensures proper response format)
    return {"access_token": access_token, "token_type": "bearer"}
