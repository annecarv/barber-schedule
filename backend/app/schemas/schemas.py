from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserRead(BaseModel):
    sub: str
    name: Optional[str]
    email: Optional[str]
    role: Optional[str]

class PostCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[List[str]] = []

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author_sub: str
    created_at: datetime
    updated_at: Optional[datetime]
    category: Optional[str]
    tags: Optional[List[str]]
    likes: int = 0

class CommentCreate(BaseModel):
    content: str

class CommentRead(BaseModel):
    id: int
    post_id: int
    author_sub: str
    content: str
    created_at: datetime
    hidden: bool

class CategoryCreate(BaseModel):
    name: str

class TagRead(BaseModel):
    id: int
    name: str
