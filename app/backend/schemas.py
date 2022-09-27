from pydantic import BaseModel, Field


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
    username: str
    password: str = Field(..., min_length=5, max_length=25)


class UserOut(BaseModel):
    id: int
    username: str


class SystemUser(UserOut):
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None