from fastapi import FastAPI,Depends
from fastapi.responses import HTMLResponse
from schemas import User_Response,Create_User
from sqlalchemy.orm import Session
from database import Base,engine,get_db
from models import User,Post
import uvicorn

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/",response_class=HTMLResponse)
async def welcome():
    return "<h1> Welcome ! </h1>"

@app.get("/users",response_model=list[User_Response])
async def get_users(skip: int=0, limit : int=10,db:Session=Depends(get_db)):
    pass



if __name__ == "__main__":
    uvicorn.run("main:app",
    host="localhost", reload=True)