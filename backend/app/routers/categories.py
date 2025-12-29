from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user, has_role, TokenData
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import Category
from app.schemas.schemas import CategoryCreate

router = APIRouter()

@router.post("", status_code=201)
async def create_category(payload: CategoryCreate, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if not has_role(token, ["ADMIN"]):
        raise HTTPException(status_code=403, detail="Only ADMIN can create categories")
    q = select(Category).where(Category.name == payload.name)
    r = await session.exec(q)
    if r.one_or_none():
        raise HTTPException(status_code=400, detail="Category exists")
    cat = Category(name=payload.name)
    session.add(cat)
    await session.commit()
    await session.refresh(cat)
    return {"id": cat.id, "name": cat.name}

@router.put("/{cat_id}")
async def edit_category(cat_id: int, payload: CategoryCreate, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if not has_role(token, ["ADMIN"]):
        raise HTTPException(status_code=403, detail="Only ADMIN can edit categories")
    q = select(Category).where(Category.id == cat_id)
    r = await session.exec(q)
    cat = r.one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    cat.name = payload.name
    session.add(cat)
    await session.commit()
    return {"status": "ok"}

@router.delete("/{cat_id}")
async def delete_category(cat_id: int, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if not has_role(token, ["ADMIN"]):
        raise HTTPException(status_code=403, detail="Only ADMIN can delete categories")
    q = select(Category).where(Category.id == cat_id)
    r = await session.exec(q)
    cat = r.one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(cat)
    await session.commit()
    return {"status": "deleted"}
