from pydantic import BaseModel

# Declaring a schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True
