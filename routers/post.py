from typing import Optional, List
from sqlalchemy.exc import IntegrityError
import models
import oauth2
from schemas import PostResponse,PostCreate,PostBase
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from database import get_db
from utils import hashPassword
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/posts",tags=["Posts"]
    )

@router.get("/", response_model=List[PostResponse])
async def get_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.getCurrentUser),
    limit: Optional[int] = 10,  # Default to 10 posts
    skip: Optional[int] = 0,    # For pagination
    search: Optional[str] = None  # For searching
):
    """
    Get all posts with optional filtering and pagination
    
    - **limit**: Number of posts to return (default: 10)
    - **skip**: Number of posts to skip (for pagination)
    - **search**: Search term to filter posts by title
    """
    
    # Build query
    query = db.query(models.Post)
    
    # Add search filter if provided
    if search:
        query = query.filter(models.Post.title.contains(search))
    
    # Apply pagination
    posts = query.offset(skip).limit(limit).all()
    
    return posts
    

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser)):
    print(current_user.email)
    new_post = models.Post(**post.dict(),owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
        # cursor.execute(
        #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        #     (post.title, post.content, post.published),
        # )
         
        # new_post = cursor.fetchone()
        # conn.commit()
        
        
    return new_post
     
    
@router.get("/{id}", response_model = PostResponse)
async def get_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser)):
    
        # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
        # post = cursor.fetchone()
        
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        
        return post
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.getCurrentUser)  # Renamed to current_user for clarity
):
    # Find the post by ID
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    
    # Check if the current user owns this post
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    
    # Delete the post
    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    


@router.put("/{id}", response_model=PostResponse)
def update_post(
    id: int, 
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.getCurrentUser)
):
    # Find the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    
    if existing_post is None:
        # Log failed attempt
        logger.warning(f"Update failed - Post not found. User ID: {current_user}, Post ID: {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {id} does not exist"
        )
    
    # Check ownership
    if existing_post.owner_id != current_user:
        # Log unauthorized attempt
        logger.warning(
            f"Unauthorized update attempt. "
            f"User ID: {current_user} tried to update Post ID: {id} "
            f"(owned by User ID: {existing_post.owner_id})"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )
    
    # Update the post
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    
    db.commit()
    db.refresh(existing_post)
    
    # Log successful update
    logger.info(f"Post updated successfully. User ID: {current_user}, Post ID: {id}")
    
    return existing_post

