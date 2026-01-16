from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceCreate(BaseModel):
    name: str
    duration: str
    price: str
    description: Optional[str] = None
    active: bool = True


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    duration: Optional[str] = None
    price: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None


class ServiceRead(BaseModel):
    id: int
    name: str
    duration: str
    price: str
    description: Optional[str]
    active: bool
    created_at: datetime


class BarberCreate(BaseModel):
    name: str
    email: str
    password: str
    specialty: Optional[str] = None
    active: bool = True


class BarberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    specialty: Optional[str] = None
    active: Optional[bool] = None


class BarberRead(BaseModel):
    id: int
    name: str
    email: str
    specialty: Optional[str]
    active: bool
    created_at: datetime


class BookingCreate(BaseModel):
    customer_name: str
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    service_id: int
    barber_id: int
    booking_date: str
    booking_time: str


class BookingUpdate(BaseModel):
    status: Optional[str] = None
    booking_date: Optional[str] = None
    booking_time: Optional[str] = None


class BookingRead(BaseModel):
    id: int
    customer_name: str
    customer_email: Optional[str]
    customer_phone: Optional[str]
    service_id: int
    service_name: str
    service_duration: str
    service_price: str
    barber_id: int
    barber_name: str
    booking_date: str
    booking_time: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
