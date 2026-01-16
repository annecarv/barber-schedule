from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta

from app.database import get_session
from app.models.models import Barber
from app.auth import (
    Token,
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter()


class BarberRegister(BaseModel):
    name: str
    email: str
    password: str
    specialty: Optional[str] = None


class BarberLogin(BaseModel):
    email: str
    password: str


@router.post("/register", status_code=201)
async def register(payload: BarberRegister, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Barber).where(Barber.email == payload.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email ja cadastrado")

    barber = Barber(
        name=payload.name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        specialty=payload.specialty,
        active=True,
    )
    session.add(barber)
    await session.commit()
    await session.refresh(barber)

    return {"message": "Barbeiro cadastrado com sucesso", "barber_id": barber.id}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Barber).where(Barber.email == form_data.username))
    barber = result.scalar_one_or_none()

    if not barber or not verify_password(form_data.password, barber.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not barber.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Conta desativada",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": barber.email, "barber_id": barber.id},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
