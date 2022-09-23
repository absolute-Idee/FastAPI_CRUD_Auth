from typing import Union
from fastapi import FastAPI, HTTPException
from .models import Post


app = FastAPI()

posts = [
    {
        "id":1,
        "title":"war",
        "text":"sdadawdasdawdaw"
    }
]

@app.get("/posts")
async def get_posts() -> dict:
    return posts

@app.get("/posts/{post_id}")
async def get_posts_id(post_id: int) -> dict:
    if post_id > len(posts):
        raise HTTPException(status_code=404, detail="No such id")
    else:
        for post in posts:
            if post['id'] == post_id:
                return {"response": post}

@app.post("/posts")
async def add_post(post: Post) -> dict:
    post.id = len(posts)+1
    posts.append(post.dict())
    return {"response": "Post added"}

@app.put("/posts/{post_id}")
async def update_post(post: Post) -> dict:
    if post.id > len(posts):
        raise HTTPException(status_code=404, detail="No such id")
    else:
        for elem in posts:
            if elem['id'] == post.id:
                elem['title'] = post.title
                elem['text'] = post.text
                return {"response": elem}

@app.delete("/posts/delete/{post_id}")
async def delete_post(post_id: int) -> dict:
    if post_id > len(posts):
        raise HTTPException(status_code=404, detail="No such id")
    else:
        for elem in posts:
            if elem['id'] == post_id:
                posts.remove(elem)
                return {"response": posts}