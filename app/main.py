
from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import HTMLResponse
from .schemas import User_Response,Create_User,Update_User
from sqlalchemy.orm import Session
from .database import Base,engine,get_db
from .models import User,Post
from . import crud
import uvicorn

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/",response_class=HTMLResponse)
async def welcome():
    return "<h1> Welcome ! </h1>"


@app.get("/users/all",response_model=list[User_Response])
async def get_users(skip:int=1,limit: int=10,
         db:Session = Depends(get_db)):
    
    return crud.get_users(db,skip =skip,limit =limit)

    
@app.get("/user{id}",response_model=User_Response)
async def get_user(user_id=int,db: Session=Depends(get_db)):
    
      user=db.query(User).filter(User.id == user_id).first()
      
      if not user:
           raise HTTPException(status_code=404,detail="User not found")
      
      return user
  
@app.post("/create_users",response_model=User_Response)
async def create_user(u_create: Create_User,db: Session = Depends(get_db)):
    
    # Check if email already exists : 
    email_exist=db.query(User).filter(User.email==User.email).first()
    # If it exists, it raises an error.
    if email_exist:
        raise HTTPException(status_code=400,detail='Email already exists')

    return crud.create_user(db,u_create)


@app.put("/users/{id}",response_model=User_Response)
async def update_user(update_u:Update_User,id,db:Session=Depends(get_db)):
    
    user=crud.update_user(db,update_u,id)
    
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    
    return user
    
    
     
  
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)