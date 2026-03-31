from datetime import UTC,datetime,timedelta
from pwdlib import PasswordHash
from fastapi import Depends,FastAPI,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError,jwt
from passlib.context import CryptContext
from .config import settings
from dotenv import load_dotenv
import os


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    """ It compares the password with the hashed password """
    return password_hash.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta:timedelta | None = None) -> str:
    """ Create a JWT acces token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC)+ timedelta(
            minutes = settings.access_token_expires_minutes,
        )
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm = settings.algorithm,
    )
    return encoded_jwt # returns JWT acces token.


load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise Exception("Invalid token")

        return user_id

    except JWTError:
        raise Exception("Invalid token")



