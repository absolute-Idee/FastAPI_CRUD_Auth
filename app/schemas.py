from lib2to3.pytree import Base
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass