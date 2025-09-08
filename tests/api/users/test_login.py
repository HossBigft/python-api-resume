import pytest

from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_access_token(client: AsyncClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    result = await client.post("/login/access-token", data=login_data)
    print("/login/access-token")
    tokens = result.json()
    assert result.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


@pytest.mark.asyncio
async def test_get_access_token_incorrect_password(client: AsyncClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    r = await client.post("/login/access-token", data=login_data)
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_use_access_token(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    r = await client.post(
        "/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
