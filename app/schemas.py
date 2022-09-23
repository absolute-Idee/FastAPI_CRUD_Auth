from lib2to3.pytree import Base
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    text: str

    class Config:
        orm_mode = True