import importlib
import pytest
from app.auth import TokenData


@pytest.mark.asyncio
async def test_create_post_and_list(client):
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    payload = {"title": "Hello", "content": "World", "category": "General", "tags": ["tag1", "tag2"]}
    resp = await client.post("/posts", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Hello"
    # list posts
    resp2 = await client.get("/posts")
    assert resp2.status_code == 200
    items = resp2.json()
    assert any(p["title"] == "Hello" for p in items)

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_like_post_and_prevent_double_like(client):
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    resp_posts = await client.get("/posts")
    posts = resp_posts.json()
    assert posts
    post_id = posts[0]["id"]
    r = await client.post(f"/posts/{post_id}/like")
    assert r.status_code == 200
    # second like should fail
    r2 = await client.post(f"/posts/{post_id}/like")
    assert r2.status_code == 400

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_comment_and_like_and_moderation_rules(client):
    # create comment as USER
    async def fake_user():
        return TokenData(sub="auth0|user2", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    resp_posts = await client.get("/posts")
    posts = resp_posts.json()
    assert posts
    post_id = posts[0]["id"]
    # create comment
    r = await client.post(f"/{post_id}/comments", json={"content": "Nice post"})
    assert r.status_code == 200
    c = r.json()
    assert c["content"] == "Nice post"
    comment_id = c["id"]
    # like comment
    rl = await client.post(f"/comments/{comment_id}/like")
    assert rl.status_code == 200
    # like again should fail
    rl2 = await client.post(f"/comments/{comment_id}/like")
    assert rl2.status_code == 400

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)

    # create a post as ADMIN
    async def fake_admin():
        return TokenData(sub="auth0|admin1", roles=["ADMIN"])

    client.app.dependency_overrides[auth_mod.get_current_user] = fake_admin
    payload = {"title": "Admin Post", "content": "Secret", "category": "AdminCat", "tags": []}
    resp = await client.post("/posts", json=payload)
    assert resp.status_code == 200
    admin_post = resp.json()
    admin_post_id = admin_post["id"]

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)

    # attempt to delete admin post as MODERATOR -> should be forbidden
    async def fake_moderator():
        return TokenData(sub="auth0|mod1", roles=["MODERATOR"])

    client.app.dependency_overrides[auth_mod.get_current_user] = fake_moderator
    rd = await client.delete(f"/posts/{admin_post_id}")
    assert rd.status_code == 403

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)
