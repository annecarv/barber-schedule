from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import posts, comments, categories, tags, users, services, barbers, bookings
from app.database import init_db

app = FastAPI(title="Barbershop & Community API")

# CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Community API routes
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, tags=["comments"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Barbershop API routes
app.include_router(services.router, prefix="/api/services", tags=["barbershop-services"])
app.include_router(barbers.router, prefix="/api/barbers", tags=["barbershop-barbers"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["barbershop-bookings"])

@app.on_event("startup")
async def on_startup():
    await init_db()
