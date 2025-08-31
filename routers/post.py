from typing import Optional, List
from sqlalchemy.exc import IntegrityError
import models
import oauth2
from schemas import PostResponse,PostCreate,PostBase
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from database import get_db
from utils import hashPassword


router = APIRouter(
    prefix="/posts",tags=["Posts"]
    )

@router.get("/", response_model = list[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    
       
        # cursor.execute("""SELECT * FROM posts;""")
        # posts = cursor.fetchall()
        
    posts = db.query(models.Post).all()
    return  posts
    

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= PostResponse)
async def create_post(post: PostCreate, db: Session = Depends(get_db),user_id: int = Depends(oauth2.getCurrentUser)):
    print(user_id)
    new_post = models.Post(**post.dict())
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
async def get_post(id: int,db: Session = Depends(get_db)):
    
        # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
        # post = cursor.fetchone()
        
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        
        return post
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),user_id: int = Depends(oauth2.getCurrentUser)):
        deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
   
        # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
        # deleted_post = cursor.fetchone()
        # conn.commit()
        if deleted_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        db.delete(deleted_post)
        db.commit()
        
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db),user_id: int = Depends(oauth2.getCurrentUser)):
        # cursor.execute(
        #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        #     (post.title, post.content, post.published, str(id)),
        # )
        # updated_post = cursor.fetchone()
        # conn.commit()
        post_query = db.query(models.Post).filter(models.Post.id == id)
        existing_post = post_query.first()
         
        if existing_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
        existing_post.title = post.title
        existing_post.content = post.content
        existing_post.published = post.published
        db.commit()
        db.refresh(existing_post)
        return existing_post

