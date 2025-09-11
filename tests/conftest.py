import pytest_asyncio
import pytest

from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from collections.abc import AsyncGenerator

from app.core.config import settings
from app.core.db import engine, Session
from app.main import app
from app.schemas import UserCreate
from app.db.models import User, Base
from tests.utils.utils import (
    get_superuser_token_headers,
    create_random_user,
    user_authentication_headers,
)


TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def db():
    """Yield a clean DB session with rollback for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, db):
    def _get_db():
        try:
            yield db
        finally:
            pass

    monkeypatch.setattr("app.core.dependencies.get_db", _get_db)


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[
    AsyncClient,
    None,
]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test" + settings.API_V1_STR
    ) as c:
        yield c


@pytest_asyncio.fixture
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest_asyncio.fixture
async def normal_user_credentials(db: Session) -> UserCreate:
    user: User = (
        db.execute(select(User).where(User.is_superuser.is_(False))).scalars().first()
    )
    if not user:
        user = create_random_user(db)
    return user


@pytest_asyncio.fixture
async def normal_user(db: Session, normal_user_credentials: UserCreate) -> User:
    user: User = (
        db.execute(select(User).where(User.email == normal_user_credentials.email))
        .scalars()
        .first()
    )
    if not user:
        user = create_random_user(db)
    return user


@pytest_asyncio.fixture
async def normal_user_token_headers(client: AsyncClient, db: Session) -> dict[str, str]:
    normal_user: UserCreate = create_random_user(db)
    return await user_authentication_headers(
        client=client, email=normal_user.email, password=normal_user.password
    )
