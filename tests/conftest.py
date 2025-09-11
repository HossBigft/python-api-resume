import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import Session
from sqlalchemy import delete, select
from collections.abc import AsyncGenerator

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.schemas import UserCreate
from app.db.models import User, Resume
from app.db.crud import create_user
from tests.utils.utils import (
    get_superuser_token_headers,
    create_random_user,
    user_authentication_headers,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[Session, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(User)
        session.execute(statement)
        session.commit()
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        create_user(session=session, user_create=user_in)


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[
    AsyncClient,
    None,
]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test" + settings.API_V1_STR
    ) as c:
        yield c


@pytest_asyncio.fixture(scope="module")
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_token_headers(client)


@pytest_asyncio.fixture(scope="module")
async def normal_user_credentials(db: Session) -> UserCreate:
    user: User = (
        db.execute(select(User).where(User.is_superuser.is_(False))).scalars().first()
    )
    if not user:
        user = create_random_user(db)
    return user


@pytest_asyncio.fixture(scope="module")
async def normal_user(db: Session, normal_user_credentials: UserCreate) -> User:
    user: User = (
        db.execute(select(User).where(User.email == normal_user_credentials.email))
        .scalars()
        .first()
    )
    if not user:
        user = create_random_user(db)
    return user


@pytest_asyncio.fixture(scope="module")
async def normal_user_token_headers(client: AsyncClient, db: Session) -> dict[str, str]:
    normal_user: UserCreate = create_random_user(db)
    return await user_authentication_headers(
        client=client, email=normal_user.email, password=normal_user.password
    )


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_resumes(db: Session):
    yield
    db.execute(delete(Resume))
    db.commit()
