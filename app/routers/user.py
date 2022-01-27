from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from .. import models, schema, utils
from .. database import get_db


# router for getting the app
router = APIRouter(
    prefix="/users",    # prefix that is common endpoint for all of the requests
    tags=["Users"]      # tags that is the name / tag given to the swaager ui in api docs
)


# creating a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)   # takeing hash password from tils class
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# getting the perticular user data
@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # user db query
    user = db.query(models.User).filter(models.User.id == id).first()

    # if user not found raise exception
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id}")

    return user