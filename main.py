
from fastapi import FastAPI,status, Response, HTTPException, Depends
from fastapi.params import Body
import models
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from sqlalchemy.orm import Session
from database import engine, get_db
from schemas import PostBase, PostCreate, PostResponse, UserCreate, UserCreateResponse
from sqlalchemy.exc import IntegrityError
from utils import hashPassword
from routers import post, user, auth 




models.Base.metadata.create_all(bind=engine)



app = FastAPI()




   
    
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="cheetohan1@", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)
        time.sleep(2)
        

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite foods", "content": "I like pizza", "id": 2}]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
async def root():
    return {"message": "successfully created a post"} 


  