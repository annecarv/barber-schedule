from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.auth import get_current_user, has_role, TokenData
from app.schemas.schemas import PostCreate, PostRead
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import Post, User, Category, Tag, PostTag, Like
from datetime import datetime

router = APIRouter()

@router.post("", response_model=PostRead)
async def create_post(payload: PostCreate, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # ensure user exists or create lightweight profile
    q = select(User).where(User.sub == token.sub)
    r = await session.exec(q)
    user = r.one_or_none()
    if not user:
        user = User(sub=token.sub, name=None, email=None, role=(token.roles[0] if token.roles else "USER"))
        session.add(user)
        await session.commit()
        await session.refresh(user)
    # category
    category = None
    if payload.category:
        q = select(Category).where(Category.name == payload.category)
        r = await session.exec(q)
        category = r.one_or_none()
        if not category:
            category = Category(name=payload.category)
            session.add(category)
            await session.commit()
            await session.refresh(category)
    post = Post(title=payload.title, content=payload.content, author_id=user.id, created_at=datetime.utcnow(), category_id=(category.id if category else None))
    session.add(post)
    await session.commit()
    await session.refresh(post)
    # tags
    tags_list = []
    for tag_name in payload.tags or []:
        if not tag_name:
            continue
        q = select(Tag).where(Tag.name == tag_name)
        r = await session.exec(q)
        tag = r.one_or_none()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            await session.commit()
            await session.refresh(tag)
        # create PostTag
        pt = PostTag(post_id=post.id, tag_id=tag.id)
        session.add(pt)
        await session.commit()
        tags_list.append(tag_name)
    return PostRead(id=post.id, title=post.title, content=post.content, author_sub=token.sub, created_at=post.created_at, updated_at=post.updated_at, category=(category.name if category else None), tags=tags_list, likes=0)

@router.get("", response_model=List[PostRead])
async def list_posts(limit: int = 10, offset: int = 0, q: Optional[str] = Query(None), category: Optional[str] = None, tag: Optional[str] = None, author_sub: Optional[str] = None, order_by: Optional[str] = None, session: AsyncSession = Depends(get_session)):
    stmt = select(Post)
    if q:
        stmt = stmt.where((Post.title.contains(q)) | (Post.content.contains(q)))
    if category:
        # join category
        stmt = stmt.where(Post.category_id != None)
    if author_sub:
        # join user
        pass
    stmt = stmt.offset(offset).limit(limit)
    r = await session.exec(stmt)
    posts = r.all()
    result = []
    for p in posts:
        # count likes
        ql = select(Like).where(Like.post_id == p.id)
        rl = await session.exec(ql)
        likes_count = len(rl.all())
        # tags
        qtags = select(Tag).join(PostTag, Tag.id == PostTag.tag_id).where(PostTag.post_id == p.id)
        rt = await session.exec(qtags)
        tags = [t.name for t in rt.all()]
        author = None
        if p.author_id:
            qa = select(User).where(User.id == p.author_id)
            ra = await session.exec(qa)
            author = ra.one_or_none()
        result.append(PostRead(id=p.id, title=p.title, content=p.content, author_sub=(author.sub if author else ""), created_at=p.created_at, updated_at=p.updated_at, category=(None if not p.category_id else ""), tags=tags, likes=likes_count))
    return result

@router.put("/{post_id}")
async def edit_post(post_id: int, payload: PostCreate, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # find post
    q = select(Post).where(Post.id == post_id)
    r = await session.exec(q)
    post = r.one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # check ownership or role
    if post.author_id is None:
        raise HTTPException(status_code=400, detail="Post has no author")
    qa = select(User).where(User.id == post.author_id)
    ra = await session.exec(qa)
    author = ra.one()
    if author.sub != token.sub and not has_role(token, ["MODERATOR", "ADMIN"]):
        raise HTTPException(status_code=403, detail="Not allowed")
    post.title = payload.title
    post.content = payload.content
    post.updated_at = datetime.utcnow()
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return {"status": "ok"}

@router.delete("/{post_id}")
async def delete_post(post_id: int, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    q = select(Post).where(Post.id == post_id)
    r = await session.exec(q)
    post = r.one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    qa = select(User).where(User.id == post.author_id)
    ra = await session.exec(qa)
    author = ra.one()
    if author.sub != token.sub and not has_role(token, ["MODERATOR", "ADMIN"]):
        raise HTTPException(status_code=403, detail="Not allowed")
    await session.delete(post)
    await session.commit()
    return {"status": "deleted"}

@router.post("/{post_id}/like")
async def like_post(post_id: int, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # ensure user
    qu = select(User).where(User.sub == token.sub)
    ru = await session.exec(qu)
    user = ru.one_or_none()
    if not user:
        user = User(sub=token.sub, role=(token.roles[0] if token.roles else "USER"))
        session.add(user)
        await session.commit()
        await session.refresh(user)
    # check existing like
    ql = select(Like).where(Like.post_id == post_id, Like.user_id == user.id)
    rl = await session.exec(ql)
    like = rl.one_or_none()
    if like:
        raise HTTPException(status_code=400, detail="Already liked")
    like = Like(user_id=user.id, post_id=post_id)
    session.add(like)
    await session.commit()
    return {"status": "liked"}
