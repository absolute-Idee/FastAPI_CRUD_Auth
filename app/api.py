from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .auth.utils import get_hashed_password

from . import crud, models
from .database import SessionLocal, engine

from .schemas import Post, PostBase, UserOut, UserAuth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup", summary='Create new user')
async def create_user(user: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user.password = get_hashed_password(user.password)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", summary='Create access and refresh tokens')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data.username)


@app.get("/posts", tags=["api"])
async def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> dict:
    return crud.get_all_posts(db, skip=skip, limit=limit)


@app.get("/posts/{post_id}", tags=["api"])
async def get_post(post_id: int, db: Session = Depends(get_db)) -> dict:
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return db_post


@app.post("/posts", status_code=201, tags=["api"])
async def add_post(post: Post, db: Session = Depends(get_db)) -> dict:
    return crud.create_post(db, post=post)


@app.put("/posts/{post_id}", tags=["api"])
async def update_post(post_id: int, post: PostBase, db: Session = Depends(get_db)) -> dict:
    return crud.update_or_create_post(db, post_id=post_id, post=post)


@app.delete("/posts/delete/{post_id}", status_code=204, tags=["api"])
async def delete_post(post_id: int, db: Session = Depends(get_db)) -> dict:
    return crud.delete_by_id(db, post_id=post_id)
