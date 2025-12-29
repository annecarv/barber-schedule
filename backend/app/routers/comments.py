from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user, has_role, TokenData
from app.schemas.schemas import CommentCreate, CommentRead
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models.models import Comment, Post, User, Like

router = APIRouter()

@router.post("/{post_id}/comments", response_model=CommentRead)
async def create_comment(post_id: int, payload: CommentCreate, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # check post
    qp = select(Post).where(Post.id == post_id)
    rp = await session.exec(qp)
    post = rp.one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    qu = select(User).where(User.sub == token.sub)
    ru = await session.exec(qu)
    user = ru.one_or_none()
    if not user:
        user = User(sub=token.sub, role=(token.roles[0] if token.roles else "USER"))
        session.add(user)
        await session.commit()
        await session.refresh(user)
    comment = Comment(post_id=post_id, author_id=user.id, content=payload.content)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return CommentRead(id=comment.id, post_id=comment.post_id, author_sub=token.sub, content=comment.content, created_at=comment.created_at, hidden=comment.hidden)

@router.post("/comments/{comment_id}/like")
async def like_comment(comment_id: int, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    qu = select(User).where(User.sub == token.sub)
    ru = await session.exec(qu)
    user = ru.one_or_none()
    if not user:
        user = User(sub=token.sub, role=(token.roles[0] if token.roles else "USER"))
        session.add(user)
        await session.commit()
        await session.refresh(user)
    ql = select(Like).where(Like.comment_id == comment_id, Like.user_id == user.id)
    rl = await session.exec(ql)
    like = rl.one_or_none()
    if like:
        raise HTTPException(status_code=400, detail="Already liked")
    like = Like(user_id=user.id, comment_id=comment_id)
    session.add(like)
    await session.commit()
    return {"status": "liked"}

@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    qc = select(Comment).where(Comment.id == comment_id)
    rc = await session.exec(qc)
    comment = rc.one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    qu = select(User).where(User.id == comment.author_id)
    ru = await session.exec(qu)
    author = ru.one()
    if author.sub != token.sub and not has_role(token, ["MODERATOR", "ADMIN"]):
        raise HTTPException(status_code=403, detail="Not allowed")
    await session.delete(comment)
    await session.commit()
    return {"status": "deleted"}

@router.put("/comments/{comment_id}/hide")
async def hide_comment(comment_id: int, token: TokenData = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if not has_role(token, ["MODERATOR", "ADMIN"]):
        raise HTTPException(status_code=403, detail="Not allowed")
    qc = select(Comment).where(Comment.id == comment_id)
    rc = await session.exec(qc)
    comment = rc.one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.hidden = True
    session.add(comment)
    await session.commit()
    return {"status": "hidden"}
