import os
import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture(scope="function")
async def client(tmp_path, monkeypatch):
    # create a fresh sqlite file per test
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_path}")

    # Import app
    from app.main import app
    from app.database import init_db

    # Initialize database for this test
    await init_db()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        ac.app = app  # Add app reference to client for dependency overrides
        yield ac

    # Clean up dependency overrides
    app.dependency_overrides.clear()
