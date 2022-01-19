from sqlalchemy import create_engine, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQL ALCHEMY URL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgre123@localhost/fastapi'

# code required for db connection 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# getting the db connection / session
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()



