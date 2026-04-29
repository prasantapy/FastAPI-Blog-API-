from fastapi import HTTPException,APIRouter,Depends
from app.database import get_db   
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.deps import get_db
from app.auth import get_current_user   

router = APIRouter(prefix="/posts")


# 👈 ADD THIS

router = APIRouter(prefix="/posts")

@router.post("/")
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud.create_post(db, post.title, post.content, user.id)


@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return {"message": "DB connected"}

def update_post(
    post_id:int,
    post:schemas.PostCreate,
    db:Session=Depends(get_db),
    user =Depends(get_current_user)
):
    result = crud.update_post(db, post_id, post.title, post.content, user.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed")

    return result


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    result = crud.delete_post(db, post_id, user.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed")

    return {"message": "Post deleted"}