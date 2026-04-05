from datetime import UTC,datetime,timedelta
from pwdlib import PasswordHash
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError,jwt
from .config import settings
from dotenv import load_dotenv
import os


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

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


def get_current_user(token: str = Depends(oauth2_scheme)):
    """We a use our variables .env from our class settings,
    instead of passing it directly from load dotenv()"""
    
    try:
        payload = jwt.decode(token,
                             settings.secret_key.get_secret_value(),algorithms=[settings.algorithm])
        user_id =payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401,detail="Invalid Token")

        return user_id
    

    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")

