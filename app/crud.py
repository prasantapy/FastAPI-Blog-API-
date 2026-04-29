from sqlalchemy.orm import Session
from app import models
from app.auth import hash_password


def create_user(db, email, password):
    print("TYPE:", type(password))
    print("VALUE:", password)
    print("LENGTH:", len(str(password)))

    user = models.User(
        email=email,
        password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user# ✅ return user directly


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def update_post(db: Session, post_id: int, title: str, content: str):
    post = get_post_by_id(db, post_id)
    if post:
        post.title = title
        post.content = content
        db.commit()
        db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    post = get_post_by_id(db, post_id)
    if post:
        db.delete(post)
        db.commit()
    return post