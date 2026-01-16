import importlib
import pytest
from app.auth import TokenData


@pytest.mark.asyncio
async def test_categories_crud(client):
    """Test creating, editing, and deleting categories (ADMIN only)"""
    async def fake_admin():
        return TokenData(sub="auth0|admin1", roles=["ADMIN"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_admin

    # Create category
    resp = await client.post("/categories", json={"name": "Technology"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Technology"
    cat_id = data["id"]

    # Try to create duplicate
    resp2 = await client.post("/categories", json={"name": "Technology"})
    assert resp2.status_code == 400

    # Edit category
    resp3 = await client.put(f"/categories/{cat_id}", json={"name": "Tech"})
    assert resp3.status_code == 200

    # Delete category
    resp4 = await client.delete(f"/categories/{cat_id}")
    assert resp4.status_code == 200

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_categories_require_admin(client):
    """Test that non-admin users cannot manage categories"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Try to create category as USER
    resp = await client.post("/categories", json={"name": "ShouldFail"})
    assert resp.status_code == 403

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_list_tags(client):
    """Test listing tags (no auth required)"""
    # Create a post with tags first
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create post with tags
    payload = {"title": "Test", "content": "Content", "category": "General", "tags": ["python", "fastapi"]}
    await client.post("/posts", json=payload)

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)

    # List tags (no auth needed)
    resp = await client.get("/tags")
    assert resp.status_code == 200
    tags = resp.json()
    assert isinstance(tags, list)
    tag_names = [t["name"] for t in tags]
    assert "python" in tag_names
    assert "fastapi" in tag_names


@pytest.mark.asyncio
async def test_search_posts(client):
    """Test post search functionality"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create posts
    await client.post("/posts", json={"title": "Python Tutorial", "content": "Learn Python", "category": "Education", "tags": []})
    await client.post("/posts", json={"title": "JavaScript Guide", "content": "Learn JS", "category": "Education", "tags": []})

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)

    # Search for "Python"
    resp = await client.get("/posts/search?q=Python")
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) >= 1
    assert any("Python" in p["title"] for p in results)

    # Search for "JavaScript"
    resp2 = await client.get("/posts/search?q=JavaScript")
    assert resp2.status_code == 200
    results2 = resp2.json()
    assert any("JavaScript" in p["title"] for p in results2)


@pytest.mark.asyncio
async def test_edit_post(client):
    """Test editing a post"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create post
    resp = await client.post("/posts", json={"title": "Original", "content": "Original content", "category": "Test", "tags": []})
    assert resp.status_code == 200
    post = resp.json()
    post_id = post["id"]

    # Edit post
    resp2 = await client.put(f"/posts/{post_id}", json={"title": "Updated", "content": "Updated content", "category": "Test", "tags": []})
    assert resp2.status_code == 200

    # Verify update
    resp3 = await client.get("/posts")
    posts = resp3.json()
    updated_post = next(p for p in posts if p["id"] == post_id)
    assert updated_post["title"] == "Updated"

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_delete_post(client):
    """Test deleting a post"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create post
    resp = await client.post("/posts", json={"title": "To Delete", "content": "Will be deleted", "category": "Test", "tags": []})
    assert resp.status_code == 200
    post = resp.json()
    post_id = post["id"]

    # Delete post
    resp2 = await client.delete(f"/posts/{post_id}")
    assert resp2.status_code == 200

    # Verify deletion
    resp3 = await client.get("/posts")
    posts = resp3.json()
    assert not any(p["id"] == post_id for p in posts)

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_list_comments(client):
    """Test listing comments for a post"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create post
    resp = await client.post("/posts", json={"title": "Post with comments", "content": "Content", "category": "Test", "tags": []})
    post = resp.json()
    post_id = post["id"]

    # Create comments
    await client.post(f"/{post_id}/comments", json={"content": "Comment 1"})
    await client.post(f"/{post_id}/comments", json={"content": "Comment 2"})

    # List comments
    resp2 = await client.get(f"/{post_id}/comments")
    assert resp2.status_code == 200
    comments = resp2.json()
    assert len(comments) == 2
    assert any(c["content"] == "Comment 1" for c in comments)
    assert any(c["content"] == "Comment 2" for c in comments)

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_hide_comment(client):
    """Test hiding a comment (MODERATOR/ADMIN only)"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create post and comment
    resp = await client.post("/posts", json={"title": "Post", "content": "Content", "category": "Test", "tags": []})
    post = resp.json()
    post_id = post["id"]

    resp2 = await client.post(f"/{post_id}/comments", json={"content": "Comment to hide"})
    comment = resp2.json()
    comment_id = comment["id"]

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)

    # Try to hide as USER (should fail)
    async def fake_user2():
        return TokenData(sub="auth0|user2", roles=["USER"])

    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user2
    resp3 = await client.put(f"/comments/{comment_id}/hide")
    assert resp3.status_code == 403

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)

    # Hide as MODERATOR (should succeed)
    async def fake_mod():
        return TokenData(sub="auth0|mod1", roles=["MODERATOR"])

    client.app.dependency_overrides[auth_mod.get_current_user] = fake_mod
    resp4 = await client.put(f"/comments/{comment_id}/hide")
    assert resp4.status_code == 200

    # Verify hidden status
    resp5 = await client.get(f"/{post_id}/comments")
    comments = resp5.json()
    hidden_comment = next(c for c in comments if c["id"] == comment_id)
    assert hidden_comment["hidden"] is True

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)


@pytest.mark.asyncio
async def test_filter_posts_by_category_and_tag(client):
    """Test filtering posts by category and tag"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create posts with different categories and tags
    await client.post("/posts", json={"title": "Python Post", "content": "About Python", "category": "Programming", "tags": ["python"]})
    await client.post("/posts", json={"title": "JS Post", "content": "About JavaScript", "category": "Web", "tags": ["javascript"]})

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)

    # Filter by category
    resp = await client.get("/posts?category=Programming")
    assert resp.status_code == 200
    posts = resp.json()
    assert all(p["category"] == "Programming" for p in posts)

    # Filter by tag
    resp2 = await client.get("/posts?tag=python")
    assert resp2.status_code == 200
    posts2 = resp2.json()
    assert all("python" in p["tags"] for p in posts2)


@pytest.mark.asyncio
async def test_order_posts_by_popularity(client):
    """Test ordering posts by popularity (likes)"""
    async def fake_user():
        return TokenData(sub="auth0|user1", roles=["USER"])

    auth_mod = importlib.import_module("app.auth")
    client.app.dependency_overrides[auth_mod.get_current_user] = fake_user

    # Create two posts
    resp1 = await client.post("/posts", json={"title": "Less Popular", "content": "Content 1", "category": "Test", "tags": []})
    post1 = resp1.json()

    resp2 = await client.post("/posts", json={"title": "More Popular", "content": "Content 2", "category": "Test", "tags": []})
    post2 = resp2.json()

    # Like the second post
    await client.post(f"/posts/{post2['id']}/like")

    # Get posts ordered by popularity (descending)
    resp3 = await client.get("/posts?order_by=-popularity")
    assert resp3.status_code == 200
    posts = resp3.json()

    # The more popular post should be first
    if len(posts) >= 2:
        # Find positions of our posts
        popular_post = next((p for p in posts if p["title"] == "More Popular"), None)
        less_popular_post = next((p for p in posts if p["title"] == "Less Popular"), None)

        if popular_post and less_popular_post:
            popular_idx = posts.index(popular_post)
            less_popular_idx = posts.index(less_popular_post)
            assert popular_idx < less_popular_idx

    client.app.dependency_overrides.pop(auth_mod.get_current_user, None)
