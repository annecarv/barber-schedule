from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.schemas import BookingCreate, BookingUpdate, BookingRead
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import Booking, Service, Barber
from datetime import datetime

router = APIRouter()

def get_duration_minutes(duration: str) -> int:
    """Convert duration string to minutes"""
    if duration == "30min":
        return 30
    elif duration == "1h":
        return 60
    elif duration == "1h30min":
        return 90
    return 30

def time_to_minutes(time_str: str) -> int:
    """Convert HH:MM to minutes since midnight"""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def is_time_slot_available(
    existing_bookings: List[Booking],
    new_time: str,
    new_duration_minutes: int
) -> bool:
    """Check if a time slot is available"""
    new_start = time_to_minutes(new_time)
    new_end = new_start + new_duration_minutes

    for booking in existing_bookings:
        if booking.status == "cancelled":
            continue

        # Get the duration of the existing booking
        existing_start = time_to_minutes(booking.booking_time)
        # We need to get the service to know duration - assuming 30min if we can't access
        existing_end = existing_start + 30  # simplified for now

        # Check for overlap
        if not (new_end <= existing_start or new_start >= existing_end):
            return False

    return True

@router.post("", response_model=BookingRead, status_code=201)
async def create_booking(payload: BookingCreate, session: AsyncSession = Depends(get_session)):
    """Create a new booking"""
    # Verify service exists
    stmt_service = select(Service).where(Service.id == payload.service_id, Service.active == True)
    result_service = await session.exec(stmt_service)
    service = result_service.one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found or inactive")

    # Verify barber exists
    stmt_barber = select(Barber).where(Barber.id == payload.barber_id, Barber.active == True)
    result_barber = await session.exec(stmt_barber)
    barber = result_barber.one_or_none()
    if not barber:
        raise HTTPException(status_code=404, detail="Barber not found or inactive")

    # Check if time slot is available
    stmt_bookings = select(Booking).where(
        Booking.barber_id == payload.barber_id,
        Booking.booking_date == payload.booking_date,
        Booking.status != "cancelled"
    )
    result_bookings = await session.exec(stmt_bookings)
    existing_bookings = result_bookings.all()

    duration_minutes = get_duration_minutes(service.duration)
    if not is_time_slot_available(existing_bookings, payload.booking_time, duration_minutes):
        raise HTTPException(status_code=409, detail="Time slot not available")

    # Create booking
    booking = Booking(**payload.dict())
    session.add(booking)
    await session.commit()
    await session.refresh(booking)

    # Return booking with service and barber details
    return BookingRead(
        id=booking.id,
        customer_name=booking.customer_name,
        customer_email=booking.customer_email,
        customer_phone=booking.customer_phone,
        service_id=service.id,
        service_name=service.name,
        service_duration=service.duration,
        service_price=service.price,
        barber_id=barber.id,
        barber_name=barber.name,
        booking_date=booking.booking_date,
        booking_time=booking.booking_time,
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at
    )

@router.get("", response_model=List[BookingRead])
async def list_bookings(
    barber_id: Optional[int] = None,
    date: Optional[str] = None,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    """List bookings with optional filters"""
    stmt = select(Booking)

    if barber_id:
        stmt = stmt.where(Booking.barber_id == barber_id)
    if date:
        stmt = stmt.where(Booking.booking_date == date)
    if status:
        stmt = stmt.where(Booking.status == status)

    result = await session.exec(stmt)
    bookings = result.all()

    # Enrich with service and barber data
    enriched_bookings = []
    for booking in bookings:
        # Get service
        stmt_service = select(Service).where(Service.id == booking.service_id)
        result_service = await session.exec(stmt_service)
        service = result_service.one()

        # Get barber
        stmt_barber = select(Barber).where(Barber.id == booking.barber_id)
        result_barber = await session.exec(stmt_barber)
        barber = result_barber.one()

        enriched_bookings.append(BookingRead(
            id=booking.id,
            customer_name=booking.customer_name,
            customer_email=booking.customer_email,
            customer_phone=booking.customer_phone,
            service_id=service.id,
            service_name=service.name,
            service_duration=service.duration,
            service_price=service.price,
            barber_id=barber.id,
            barber_name=barber.name,
            booking_date=booking.booking_date,
            booking_time=booking.booking_time,
            status=booking.status,
            created_at=booking.created_at,
            updated_at=booking.updated_at
        ))

    return enriched_bookings

@router.get("/available-times")
async def get_available_times(
    barber_id: int,
    date: str,
    service_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Get available time slots for a barber on a specific date"""
    # Get service to know duration
    stmt_service = select(Service).where(Service.id == service_id)
    result_service = await session.exec(stmt_service)
    service = result_service.one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Get existing bookings for the barber on that date
    stmt = select(Booking).where(
        Booking.barber_id == barber_id,
        Booking.booking_date == date,
        Booking.status != "cancelled"
    )
    result = await session.exec(stmt)
    existing_bookings = result.all()

    # Generate all possible time slots (9:00 to 18:30 in 30-min intervals)
    all_slots = []
    for hour in range(9, 19):
        all_slots.append(f"{hour:02d}:00")
        if hour < 18:  # Don't add :30 for 18h
            all_slots.append(f"{hour:02d}:30")

    # Filter available slots
    duration_minutes = get_duration_minutes(service.duration)
    available_slots = []

    for slot in all_slots:
        if is_time_slot_available(existing_bookings, slot, duration_minutes):
            # Also check if the slot + duration doesn't go past 19:00
            slot_start = time_to_minutes(slot)
            slot_end = slot_start + duration_minutes
            if slot_end <= 19 * 60:  # 19:00 in minutes
                available_slots.append(slot)

    return {"available_times": available_slots}

@router.get("/{booking_id}", response_model=BookingRead)
async def get_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    """Get a specific booking by ID"""
    stmt = select(Booking).where(Booking.id == booking_id)
    result = await session.exec(stmt)
    booking = result.one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Get service and barber
    stmt_service = select(Service).where(Service.id == booking.service_id)
    result_service = await session.exec(stmt_service)
    service = result_service.one()

    stmt_barber = select(Barber).where(Barber.id == booking.barber_id)
    result_barber = await session.exec(stmt_barber)
    barber = result_barber.one()

    return BookingRead(
        id=booking.id,
        customer_name=booking.customer_name,
        customer_email=booking.customer_email,
        customer_phone=booking.customer_phone,
        service_id=service.id,
        service_name=service.name,
        service_duration=service.duration,
        service_price=service.price,
        barber_id=barber.id,
        barber_name=barber.name,
        booking_date=booking.booking_date,
        booking_time=booking.booking_time,
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at
    )

@router.put("/{booking_id}", response_model=BookingRead)
async def update_booking(booking_id: int, payload: BookingUpdate, session: AsyncSession = Depends(get_session)):
    """Update a booking (change status, date, or time)"""
    stmt = select(Booking).where(Booking.id == booking_id)
    result = await session.exec(stmt)
    booking = result.one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Update only provided fields
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(booking, key, value)

    booking.updated_at = datetime.utcnow()
    session.add(booking)
    await session.commit()
    await session.refresh(booking)

    # Get service and barber for response
    stmt_service = select(Service).where(Service.id == booking.service_id)
    result_service = await session.exec(stmt_service)
    service = result_service.one()

    stmt_barber = select(Barber).where(Barber.id == booking.barber_id)
    result_barber = await session.exec(stmt_barber)
    barber = result_barber.one()

    return BookingRead(
        id=booking.id,
        customer_name=booking.customer_name,
        customer_email=booking.customer_email,
        customer_phone=booking.customer_phone,
        service_id=service.id,
        service_name=service.name,
        service_duration=service.duration,
        service_price=service.price,
        barber_id=barber.id,
        barber_name=barber.name,
        booking_date=booking.booking_date,
        booking_time=booking.booking_time,
        status=booking.status,
        created_at=booking.created_at,
        updated_at=booking.updated_at
    )

@router.delete("/{booking_id}")
async def cancel_booking(booking_id: int, session: AsyncSession = Depends(get_session)):
    """Cancel a booking (soft delete by setting status=cancelled)"""
    stmt = select(Booking).where(Booking.id == booking_id)
    result = await session.exec(stmt)
    booking = result.one_or_none()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = "cancelled"
    booking.updated_at = datetime.utcnow()
    session.add(booking)
    await session.commit()
    return {"status": "cancelled"}
