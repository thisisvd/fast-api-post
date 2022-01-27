import imp
from os import stat
from typing import List
from msilib.schema import PublishComponent
from multiprocessing import synchronize
from operator import mod
from passlib.context import CryptContext
from turtle import pos, title
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.param_functions import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session 
from . import models, schema, utils
from .database import engine, get_db
from . routers import post, user


# adding password encrypton algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# deciding and binding engine
models.Base.metadata.create_all(bind=engine)


# FASTAPI instance
app = FastAPI()
        

# refrencing the object post i.e. [include all function/defs from post objects]
app.include_router(post.router)


# refrencing the object user i.e. [include all function/defs from users objects]
app.include_router(user.router)


# just get the link request 
@app.get("/")
def root():
    return {"message": "Welcome to my first api that I have developed by my own!!!!"}

