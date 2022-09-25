from pydantic import BaseModel, Field
from uuid import UUID


class PostBase(BaseModel):
    title: str
    text: str


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class UserAuth(BaseModel):
    email: str
    password: str = Field(..., min_length=5, max_length=25)


class UserOut(BaseModel):
    id: UUID
    email: str
