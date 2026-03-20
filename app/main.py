from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import HTMLResponse
from schemas import User_Response,Create_User
from sqlalchemy.orm import Session
from database import Base,engine,get_db
from models import User,Post
import crud
import uvicorn

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/",response_class=HTMLResponse)
async def welcome():
    return "<h1> Welcome ! </h1>"


@app.get("/users",response_model=list[User_Response])
async def get_users(db:Session = Depends(get_db)):
    
    pass
@app.get("/user",response_model=User_Response)
async def get_user(user_id=int,db: Session=Depends(get_db)):
    
      user=db.query(User).filter(User.id == user_id).first()
      
      if not user:
          HTTPException(status_code=404,detail="User not found")
      
      return user

if __name__ == "__main__":
    uvicorn.run("main:app",
    host="localhost", reload=True)