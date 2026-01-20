from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import services, barbers, bookings, auth
from app.database import init_db

app = FastAPI(title="Barbershop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(services.router, prefix="/api/services", tags=["services"])
app.include_router(barbers.router, prefix="/api/barbers", tags=["barbers"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])

@app.on_event("startup")
async def on_startup():
    await init_db()
