from fastapi import FastAPI
from app.database import Base, engine
from app import models 
from app.routers import post,user
app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(user.router)
app.include_router(post.router)

@app.get("/")
def home():
    return {"message": "API is running"}

