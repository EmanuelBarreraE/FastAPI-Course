from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Create table posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='123456789', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfully")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
#     "title": "favorite foods", "content": "I like pizza", "id": 2}]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

@app.get("/")
async def root():
    return {"message": "Hello friend"}


#--------------------------------Getting posts with ORM Example--------------------------------#
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data": posts}
#----------------------------------------------------------------------------------------------#

    
#Getting posts with ORM
#--------------------------------Getting posts with SQL Example--------------------------------#
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}
#----------------------------------------------------------------------------------------------#

#--------------------------------Getting posts with ORM--------------------------------#
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data": posts}
#--------------------------------------------------------------------------------------#


#--------------------------------Creating posts with ORM-------------------------------#

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
#--------------------------------------------------------------------------------------#


#--------------------------------Creating posts with SQL Example-------------------------------#
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}
#----------------------------------------------------------------------------------------------#

#--------------------------------Getting one post by id with ORM-------------------------------#
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post= db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}
#-----------------------------------------------------------------------------------------------#


#--------------------------------Getting one post by id with SQL Example-------------------------------#
# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
#     post = cursor.fetchone()
#     print(post)
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     return {"post_detail": post}
#-------------------------------------------------------------------------------------------------------#

#--------------------------------Deleting one post by id with ORM-------------------------------#
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
   post = db.query(models.Post).filter(models.Post.id == id)

   if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
   post.delete(synchronize_session=False)
   db.commit()
        
        
   Response(status_code=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------------------------#

#--------------------------------Deleting one post by id with SQL Example-------------------------------#
# @app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", ((id,)))
#     deleted_post = cursor.fetcone()
#     conn.commit()
    
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#-------------------------------------------------------------------------------------------------------#

#--------------------------------Updating one post by id with ORM-------------------------------#
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
         
    post_query.update(updated_post.model_dump(), synchronize_session=False )
    db.commit()   
    return {"data": post_query.first()}
#-----------------------------------------------------------------------------------------------#



#--------------------------------Updating one post by id with SQL Example-------------------------------#
# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
    
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, (id,)))
#     updated_post = cursor.fetchone()
#     conn.commit()
    
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     return {"data": updated_post}
#-------------------------------------------------------------------------------------------------------#





