from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List
from .. import models, schema
from .. database import get_db


# router for getting the app
router = APIRouter(
    prefix="/posts",   # prefix that is common endpoint for all of the requests
    tags=["Posts"]     # tags that is the name / tag given to the swaager ui in api docs
)


# get the posts from database
@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()    
    return posts


# create a new post with status code 201
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
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
@router.get("/{id}", response_model=schema.Post)
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/{id}", response_model=schema.Post)
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
