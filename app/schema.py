from pydantic import BaseModel, EmailStr
from datetime import datetime


# Post Class models         


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):

    pass


# classes for responses body

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Users class model         


class UserCreate(BaseModel):
    email: EmailStr
    password: str


# class for response body

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

    