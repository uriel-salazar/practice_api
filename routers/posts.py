from fastapi import FastAPI,Depends,HTTPException,APIRouter
from fastapi.responses import HTMLResponse
from app.schemas import Create_Post,Response_Post
from sqlalchemy.orm import Session
from app.database import Base,engine,get_db
from app.models import User,Post
from app import crud
import uvicorn
router=APIRouter()

@router.post("/posts",response_model=Response_Post)
def create_post_endpoint(post: Create_Post, db: Session = Depends(get_db)):
    return crud.create_post(db,post)