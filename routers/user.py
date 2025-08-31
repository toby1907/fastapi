from sqlalchemy.exc import IntegrityError
import models
from schemas import UserCreateResponse, UserCreate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from utils import hashPassword
router = APIRouter(
    prefix="/users", tags=["Users"]
     )



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # First check if user exists (avoids unnecessary hash operation)
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    try:
        # Hash the password and create user
        hashed_password = hashPassword(user.password)
        new_user = models.User(email=user.email, password=hashed_password)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except IntegrityError:
        db.rollback()
        # This is a backup in case of race conditions
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

@router.get("/{id}", response_model=UserCreateResponse)    
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user 