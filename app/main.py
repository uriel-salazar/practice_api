from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database import Base, engine
from routers import posts, users
import uvicorn


app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router,prefix="/users",tags=["Users"])
app.include_router(posts.router,prefix="/posts",tags=["Posts"])


@app.get("/",response_class=HTMLResponse)
async def welcome():
    return "<h1> Welcome ! </h1>"



if __name__ == "__main__":
    uvicorn.run("main:app",
    host="localhost", reload=True)