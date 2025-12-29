from fastapi import FastAPI
from app.routers import posts, comments, categories, tags
from app.database import init_db

app = FastAPI(title="Community API")

app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/posts", tags=["comments"])  # comments router uses /posts/{id}/comments
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])

@app.on_event("startup")
async def on_startup():
    await init_db()
