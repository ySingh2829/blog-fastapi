from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import IntEnum

# Schemas for User
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Schema for Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: str
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    total_votes: int


# Schemas for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]


# Schemacs for vote
class Like(IntEnum):
    remove = 0
    give = 1

class Vote(BaseModel):
    post_id: int
    dir: Like = Like.remove
