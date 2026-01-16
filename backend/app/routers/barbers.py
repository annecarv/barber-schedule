from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.schemas import BarberCreate, BarberUpdate, BarberRead
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import Barber

router = APIRouter()

@router.post("", response_model=BarberRead, status_code=201)
async def create_barber(payload: BarberCreate, session: AsyncSession = Depends(get_session)):
    """Create a new barber"""
    # Check if email already exists
    stmt = select(Barber).where(Barber.email == payload.email)
    result = await session.exec(stmt)
    existing = result.one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    barber = Barber(**payload.model_dump())
    session.add(barber)
    await session.commit()
    await session.refresh(barber)
    return barber

@router.get("", response_model=List[BarberRead])
async def list_barbers(active_only: bool = True, session: AsyncSession = Depends(get_session)):
    """List all barbers, optionally filter by active status"""
    stmt = select(Barber)
    if active_only:
        stmt = stmt.where(Barber.active == True)
    result = await session.exec(stmt)
    barbers = result.all()
    return barbers

@router.get("/{barber_id}", response_model=BarberRead)
async def get_barber(barber_id: int, session: AsyncSession = Depends(get_session)):
    """Get a specific barber by ID"""
    stmt = select(Barber).where(Barber.id == barber_id)
    result = await session.exec(stmt)
    barber = result.one_or_none()
    if not barber:
        raise HTTPException(status_code=404, detail="Barber not found")
    return barber

@router.put("/{barber_id}", response_model=BarberRead)
async def update_barber(barber_id: int, payload: BarberUpdate, session: AsyncSession = Depends(get_session)):
    """Update a barber"""
    stmt = select(Barber).where(Barber.id == barber_id)
    result = await session.exec(stmt)
    barber = result.one_or_none()
    if not barber:
        raise HTTPException(status_code=404, detail="Barber not found")

    # Check email uniqueness if updating email
    if payload.email and payload.email != barber.email:
        stmt_check = select(Barber).where(Barber.email == payload.email)
        result_check = await session.exec(stmt_check)
        if result_check.one_or_none():
            raise HTTPException(status_code=400, detail="Email already in use")

    # Update only provided fields
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(barber, key, value)

    session.add(barber)
    await session.commit()
    await session.refresh(barber)
    return barber

@router.delete("/{barber_id}")
async def delete_barber(barber_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a barber (soft delete by setting active=False)"""
    stmt = select(Barber).where(Barber.id == barber_id)
    result = await session.exec(stmt)
    barber = result.one_or_none()
    if not barber:
        raise HTTPException(status_code=404, detail="Barber not found")

    barber.active = False
    session.add(barber)
    await session.commit()
    return {"status": "deleted"}
