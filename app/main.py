from fastapi import FastAPI
from database import Base,engine
import uvicorn


app=FastAPI()


Base.metadata.create_all(bind=engine)



