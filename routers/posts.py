from fastapi import FastAPI,Depends,HTTPException,APIRouter
from fastapi.responses import HTMLResponse
from app.schemas import Create_Post,Response_Post
from sqlalchemy.orm import Session
from app.database import Base,engine,get_db
from app.models import User,Post
from app import crud
import uvicorn
router=APIRouter()

@router.post("",response_model=Response_Post)
def create_post(post: Create_Post, db: Session = Depends(get_db)):
    return crud.create_post(db,post)


@router.get("/{user_id}",response_model=Response_Post)
def get_post(user_id:int,db: Session = Depends(get_db)):
    get_one=crud.get_post(db,user_id)
    
    if get_one is None:
        HTTPException(status_code=404,detail="We couldn't find your post.")
    return get_one


@router.get("",response_model=list[Response_Post])
def get_posts(skip:int =1,limit : int=10,
    db:Session = Depends(get_db)):
    
    posts=crud.get_posts(db,skip=skip,limit=limit)
    return posts

