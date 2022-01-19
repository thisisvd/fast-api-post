from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# FASTAPI instance
app = FastAPI()


# Base class model for post 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Database connection for RAW POSTGRE SQL
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                            password='postgre123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Was sucessfull!")
        break
    except Exception as error:
        print("Connecting to db failed!")
        print("Error: ", error)
        time.sleep(2)


# get the simple api message 
@app.get("/")
def root():
    return {"message": "Welcome to my fastapi learning!!!!"}


# get the posts data from database
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


# create a new post with status code 201 and save in the db
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # stage changes
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ",
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()  
    # actually commiting changes data to database
    conn.commit()
    return {"data": new_post}


# find the post by providing an id from db and setting up the status code 
@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    cursor.execute("SELECT * FROM posts WHERE id = %s ", (str(id)))
    post = cursor.fetchone()

    # raise an exception if not found in db
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"post with id: {id} was not found"}
    
    return {"post_detail" : post}


# deleting the post from db 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find index and delete from array
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING * ", (str(id)))
    delete_post = cursor.fetchone()
    conn.commit()    

    # raise an exception if not found in db
    if delete_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id: {id} was not found")

    return {"Message": "post was sucessfully deleted!"}
    

# update a post using put in db
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ",
     (post.title, post.content, post.published, str(id)))
    update_post = cursor.fetchone()
    conn.commit()

    # raise an exception if not found in db
    if update_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id: {id} was not found")

    return {"data": update_post}
