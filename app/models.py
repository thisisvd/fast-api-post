from ast import Str
import email
from sqlalchemy import Column, Integer, String, Boolean, true
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

# BASE MODEL and TABEL architecture that has been used in this api 
class Post(Base):
    __tablename__ = "postorms"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

# User class 
class User(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,nullable=False, unique=True) # one email will not register twice
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
