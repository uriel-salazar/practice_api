from fastapi import FastAPI,Depends,HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserPublic,Create_User,Update_User,UserPrivate,Token
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from typing import Annotated
from sqlalchemy import select
from app.auth import verify_password,create_access_token,get_current_user
from app import crud
from sqlalchemy import func
import uvicorn

app= FastAPI()
router = APIRouter()




@router.get("",response_model=list[UserPublic])
async def get_users(skip:int=1,limit: int=10,
         db:Session = Depends(get_db)):
    """ Gets all user from a list of "User Response"

    Args:
        skip (int): Defaults to 1.
        limit (int):  Defaults to 10.
        db (Session): Defaults to Depends(get_db).

    Returns:
        (list) Get's a list of users 
    """
    
    return crud.get_users(db,skip =skip,limit =limit)


@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
   return {"email": current_user}
  
    
@router.get("/{id}",response_model=UserPublic)   
async def get_user(id=int,db: Session=Depends(get_db)):
    """ Finds an user by their id. If isn't founded,
    it will raise an status code of 404.

    Args:
        user_id (int): (primary key from the user's table.)
        db (Session): Database session.

    Raises:
        HTTPException: raises 404 status code 

    Returns:
        user: User founded by id.
    """
    
    user=db.query(User).filter(User.id == id).first()
      
    if not user:
           raise HTTPException(status_code=404,detail="User not found")
      
    return user
  
@router.post("",response_model=UserPrivate)
async def create_user(u_create: Create_User,db: Session = Depends(get_db)):
    """ Creates a new user 

    Args:
        u_create (Create_User): Pydantic schema for creating a new user. 
        db (Session): Database session

    Raises:
        HTTPException: raises  404 status code 

    Returns:
        The user created response.
    """
    
    # Check the existence of an email ( to avoid duplicated emails.) : 
    email_exist=db.query(User).filter(func.lower(User.email)==u_create.email.lower()).first()
    # If it exists, it raises an error.
    if email_exist:
        raise HTTPException(status_code=400,detail='Email already exists')

    return crud.create_user(db,u_create)


@router.put("/{id}",response_model=UserPublic)
async def update_user(update_u:Update_User,id,db:Session=Depends(get_db)):
    """
    Updates an user by their id.
    If user is None, it raises a 404 error.
    
    Returns:
        User updated 
    """
    
    user=crud.update_user(db,update_u,id)
    
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    return user

@router.delete("/{id}")
async def delete_user(id:int,db: Session = Depends(get_db)):
    delete=crud.delete_user(db,id)
    
    if delete is None:
        raise HTTPException(status_code=400,detail="User not found")
    
    return f"User deleted succesful!"


@router.post("/token",response_model=Token)
async def log_in_access(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session,Depends(get_db)]
):
    
  user = db.execute(
        select(User).where(func.lower(User.email) == form_data.username.lower())
    ).scalar_one_or_none()
 
  
  # If user exists 
  if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

  #Verifies the password. 
  if  not verify_password(form_data.password, user.hashed_password):
        
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
  
  # creates a token
  access_token = create_access_token(
        data={"sub": user.email}
    )

    #returns the bearer token
  return {
        "access_token": access_token,
        "token_type": "bearer"
    }
  
