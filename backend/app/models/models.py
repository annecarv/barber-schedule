from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sub: str = Field(index=True, unique=True)
    name: Optional[str]
    email: Optional[str]
    role: Optional[str] = "USER"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    posts: List["Post"] = Relationship(back_populates="author")
    comments: List["Comment"] = Relationship(back_populates="author")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    posts: List["Post"] = Relationship(back_populates="category")

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

class PostTag(SQLModel, table=True):
    post_id: Optional[int] = Field(default=None, foreign_key="post.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    author: Optional[User] = Relationship(back_populates="posts")
    category: Optional[Category] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: Optional[int] = Field(default=None, foreign_key="post.id")
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    hidden: bool = Field(default=False)

    post: Optional[Post] = Relationship(back_populates="comments")
    author: Optional[User] = Relationship(back_populates="comments")

class Like(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: Optional[int] = Field(default=None, foreign_key="post.id")
    comment_id: Optional[int] = Field(default=None, foreign_key="comment.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Barbershop models
class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    duration: str  # e.g., "30min", "1h", "1h30min"
    price: str  # e.g., "R$ 25"
    description: Optional[str] = None
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    bookings: List["Booking"] = Relationship(back_populates="service")

class Barber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    specialty: Optional[str] = None
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    bookings: List["Booking"] = Relationship(back_populates="barber")

class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    service_id: int = Field(foreign_key="service.id")
    barber_id: int = Field(foreign_key="barber.id")
    booking_date: str  # formato: "YYYY-MM-DD"
    booking_time: str  # formato: "HH:MM"
    status: str = Field(default="confirmed")  # confirmed, cancelled, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    service: Optional[Service] = Relationship(back_populates="bookings")
    barber: Optional[Barber] = Relationship(back_populates="bookings")
