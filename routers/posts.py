from fastapi import Depends,HTTPException,APIRouter,UploadFile,File,Form
from app.schemas import Create_Post,Response_Post
from sqlalchemy.orm import Session
from pathlib import Path
from routers.resize import image_resize_800
from app.database import Base,engine,get_db
from app import crud
from PIL import Image
from io import BytesIO
from app.models import User
from app.auth import get_current_user
import os,uuid
router=APIRouter()

@router.post("",response_model=Response_Post)
async def create_post_endpoint(
    description: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """  Creates a post 
    Saves the image and it finds where to store it.
    If isn't found, it raises a 500 error.
    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    
    BASE_DIR = Path(__file__).resolve().parent.parent # goes up to find the folder 
    UPLOAD_DIR = BASE_DIR / "app" / "images"
    
    #creates folder if it doesn't exist.
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 
    #creates an unique filename 
    
    # It defaults to 'None' if no image was sent.
    image_url=None 
    
    if image:
        contents=await image.read()
        i=image_resize_800(contents)
        
        filename_str = image.filename or "file.jpg"
        
        # Adds a safe file name to avoid duplicated filenames.
        safe_filename = f"{uuid.uuid4()}__{Path(filename_str).name}"
        file_location = UPLOAD_DIR / safe_filename 
        
        try:
            with open(file_location, "wb") as buffer:
                img_bytes = BytesIO()
                # turns image  object to bytes :
                i.save(img_bytes,format="JPEG",quality=85,optimize=True)  
                buffer.write(img_bytes.getvalue()) 
                image_url=str(file_location)
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
        
    return crud.create_post(
        db=db,
        description=description,
        user_id=current_user.id,
        image_url=image_url
    )

@router.get("/{user_id}",response_model=Response_Post)
def get_post(user_id:int,db: Session = Depends(get_db)):
    get_one=crud.get_post(db,user_id)
    
    if get_one is None:
        raise HTTPException(status_code=404,detail="We couldn't find your post.")
    return get_one


@router.get("",response_model=list[Response_Post])
def get_posts(skip:int =1,limit : int=10,
    db:Session = Depends(get_db)):
    
    posts=crud.get_posts(db,skip=skip,limit=limit)
    
    if posts is None:
        raise HTTPException(status_code=404,detail="No posts available.")
    return posts

