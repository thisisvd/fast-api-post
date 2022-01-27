from passlib.context import CryptContext


# adding password encrypton algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# pwd hashing algorithm
def hash(password: str):
    return pwd_context.hash(password)