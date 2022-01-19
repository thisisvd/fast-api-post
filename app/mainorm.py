from typing import List
from msilib.schema import PublishComponent
from multiprocessing import synchronize
from operator import mod
from turtle import pos, title
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.param_functions import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session 
from . import models, schema
from .database import engine, get_db


# deciding and binding engine
models.Base.metadata.create_all(bind=engine)


# FASTAPI instance
app = FastAPI()
        

# just get the link request 
@app.get("/")
def root():
    return {"message": "Welcome to my first api that I have developed by my own!!!!"}


# get the posts from database
@app.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()    
    return posts


# create a new post with status code 201
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    # creating the post 
    # *** OLD WAY OF ADDING DATA ***
    # new_post = models.Post(title=post.title,content=post.content,
    #                         published=post.published)
    # *** NEW & SHORT WAY OF ADDING DATA ***
    new_post = models.Post(**post.dict())
    db.add(new_post)        # adding the new post
    db.commit()             # committing in the db
    db.refresh(new_post)    # getting the newly created post as same as returning in sql query

    return new_post


# find the post by providing an id and setting up the status code
@app.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int,response: Response, db: Session = Depends(get_db)):
    
    # find the post by postID --- use all() if there is more elements that likely equal to be id or whatever they passed 
    post = db.query(models.Post).filter(models.Post.id == id).first() # use first() if there is a primary / only 1 equal to id 
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"post with id: {id} was not found"}
    
    return post


# deleting the post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # find the post by post id and delete it
    post = db.query(models.Post).filter(models.Post.id == id)
   
    if post.first() == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id: {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()

    return {"Message": "post was sucessfully deleted!"}
    

# update a post using put 
@app.put("/posts/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    
    # query to find post with the specific ID
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # actually grab that post 
    post = post_query.first()

    # if it doesn't exist then we run 404 
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id: {id} was not found")

    # if it update then we will update it 
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()     # commit it to the db

    return post_query.first() # we get the updated post and send it back to the user
