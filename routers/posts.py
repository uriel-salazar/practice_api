from fastapi import Depends,HTTPException,APIRouter,UploadFile,File
from app.schemas import Create_Post,Response_Post
from sqlalchemy.orm import Session
from app.database import Base,engine,get_db
from app import crud
from app.models import User
from app.auth import get_current_user
import uvicorn
from sqlalchemy import func 
import os,uuid,shutil
router=APIRouter()

@router.post("",response_model=Response_Post)
def create_post(post: Create_Post, db: Session = Depends(get_db),
        current_user=Depends(get_current_user),images:UploadFile=File(...)):

    UPLOAD_DIR = "images"

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    filename = f"{uuid.uuid4()}.jpg"
    file_path = f"{UPLOAD_DIR}/{filename}"

    # Saves the image 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(images.file, buffer)

    return crud.create_post(db,post,current_user,file_path)


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

