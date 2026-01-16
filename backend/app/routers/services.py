from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.schemas import ServiceCreate, ServiceUpdate, ServiceRead
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import Service
from datetime import datetime

router = APIRouter()

@router.post("", response_model=ServiceRead, status_code=201)
async def create_service(payload: ServiceCreate, session: AsyncSession = Depends(get_session)):
    """Create a new service"""
    service = Service(**payload.model_dump())
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service

@router.get("", response_model=List[ServiceRead])
async def list_services(active_only: bool = True, session: AsyncSession = Depends(get_session)):
    """List all services, optionally filter by active status"""
    stmt = select(Service)
    if active_only:
        stmt = stmt.where(Service.active == True)
    result = await session.exec(stmt)
    services = result.all()
    return services

@router.get("/{service_id}", response_model=ServiceRead)
async def get_service(service_id: int, session: AsyncSession = Depends(get_session)):
    """Get a specific service by ID"""
    stmt = select(Service).where(Service.id == service_id)
    result = await session.exec(stmt)
    service = result.one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=ServiceRead)
async def update_service(service_id: int, payload: ServiceUpdate, session: AsyncSession = Depends(get_session)):
    """Update a service"""
    stmt = select(Service).where(Service.id == service_id)
    result = await session.exec(stmt)
    service = result.one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Update only provided fields
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, key, value)

    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service

@router.delete("/{service_id}")
async def delete_service(service_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a service (soft delete by setting active=False)"""
    stmt = select(Service).where(Service.id == service_id)
    result = await session.exec(stmt)
    service = result.one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service.active = False
    session.add(service)
    await session.commit()
    return {"status": "deleted"}
