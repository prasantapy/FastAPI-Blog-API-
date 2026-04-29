

from fastapi import FastAPI

app=FastAPI()

from app.database import Base, engine
from blog_api import 

Base.metadata.create_all(bind=engine)