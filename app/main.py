from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from database import Base,engine
from models import User,Post
import uvicorn

app=FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/",response_class=HTMLResponse)
async def welcome():
    return "<h1> Welcome ! </h1>"



if __name__ == "__main__":
    uvicorn.run("main:app",
    host="localhost", reload=True)