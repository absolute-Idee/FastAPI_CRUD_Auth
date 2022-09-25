from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .schemas import Post, PostBase


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
async def add_post(post: schemas.Post, db: Session = Depends(get_db)) -> dict:
    return crud.create_post(db, post=post)


@app.put("/posts/{post_id}", tags=["api"])
async def update_post(post_id: int, post: PostBase, db: Session = Depends(get_db)) -> dict:
    return crud.update_or_create_post(db, post_id=post_id, post=post)


@app.delete("/posts/delete/{post_id}", status_code=204, tags=["api"])
async def delete_post(post_id: int, db: Session = Depends(get_db)) -> dict:
    return crud.delete_by_id(db, post_id=post_id)
