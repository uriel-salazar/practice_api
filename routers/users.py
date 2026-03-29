from fastapi import FastAPI,Depends,HTTPException,APIRouter
from fastapi.responses import HTMLResponse
from app.schemas import UserPublic,Create_User,Update_User,Create_Post,Response_Post
from sqlalchemy.orm import Session
from app.database import Base,engine,get_db
from app.models import User,Post
from app import crud
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
  
@router.post("",response_model=UserPublic)
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
    email_exist=db.query(User).filter(User.email==u_create.email).first()
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

@app.delete("/{id}")
def delete_user(id:int,db: Session = Depends(get_db)):
    delete=crud.delete_user(db,id)
    
    if delete is None:
        raise HTTPException(status_code=400,detail="User not found")
    
    return f"User deleted succesful!"


