from fastapi import APIRouter, Depends
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import Tag

router = APIRouter()

@router.get("", response_model=list)
async def list_tags(session: AsyncSession = Depends(get_session)):
    q = select(Tag)
    r = await session.exec(q)
    tags = r.all()
    return [{"id": t.id, "name": t.name} for t in tags]
