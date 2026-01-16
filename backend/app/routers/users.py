from fastapi import APIRouter, Depends
from app.auth import get_current_user, TokenData
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import User
from app.schemas.schemas import UserRead, UserUpdate

router = APIRouter()


def _highest_role(roles):
    if not roles:
        return "USER"
    normalized = [r.upper() for r in roles]
    if "ADMIN" in normalized:
        return "ADMIN"
    if "MODERATOR" in normalized:
        return "MODERATOR"
    return "USER"


@router.get("/me", response_model=UserRead)
async def get_me(token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.sub == token.sub)
    r = await session.exec(q)
    user = r.one_or_none()
    role_from_token = _highest_role(token.roles)
    if not user:
        user = User(sub=token.sub, role=role_from_token)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    else:
        if user.role != role_from_token:
            user.role = role_from_token
            session.add(user)
            await session.commit()
            await session.refresh(user)
    return UserRead(sub=user.sub, name=user.name, email=user.email, role=user.role)


@router.put("/me", response_model=UserRead)
async def update_me(payload: UserUpdate, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.sub == token.sub)
    r = await session.exec(q)
    user = r.one_or_none()
    role_from_token = _highest_role(token.roles)
    if not user:
        user = User(sub=token.sub, role=role_from_token)
    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = payload.email
    # always sync role from token
    user.role = role_from_token
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead(sub=user.sub, name=user.name, email=user.email, role=user.role)
