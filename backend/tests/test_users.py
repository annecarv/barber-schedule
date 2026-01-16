import os
# ensure test DB is used before app import
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_test.db")

import importlib
import pytest
from app.auth import TokenData


@pytest.mark.asyncio
async def test_get_me_creates_user(client):
    # override auth dependency on the running app
    async def fake_get_current_user():
        return TokenData(sub="auth0|u1", roles=["USER"])

    # set override
    from importlib import import_module
    auth_mod = import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_get_current_user

    resp = await client.get("/users/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sub"] == "auth0|u1"
    assert data["role"] == "USER"

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_put_me_updates_and_syncs_role(client):
    async def fake_get_current_user():
        return TokenData(sub="auth0|u1", roles=["ADMIN"])

    from importlib import import_module
    auth_mod = import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_get_current_user

    resp = await client.put("/users/me", json={"name": "Test User", "email": "test@example.com"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "ADMIN"

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)
