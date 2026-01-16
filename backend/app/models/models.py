from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    duration: str
    price: str
    description: Optional[str] = None
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    bookings: List["Booking"] = Relationship(back_populates="service")


class Barber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    password_hash: str = Field(default="")
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
    booking_date: str
    booking_time: str
    status: str = Field(default="confirmed")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    service: Optional[Service] = Relationship(back_populates="bookings")
    barber: Optional[Barber] = Relationship(back_populates="bookings")
