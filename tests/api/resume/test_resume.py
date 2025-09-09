import pytest

from httpx import AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.resume.resume_shemas import ResumeSchema
from tests.utils.utils import random_lower_string
from app.db.models import Resume, User


@pytest.mark.asyncio
async def test_create_resume(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    normal_user: User,
) -> None:
    resume = ResumeSchema(title=random_lower_string(), content=random_lower_string())
    await client.post(
        "/resume/", headers=normal_user_token_headers, json=resume.model_dump()
    )
    resume_in_db: Resume = (
        db.execute(select(Resume).where(Resume.user_id == normal_user.id))
        .scalars()
        .first()
    )
    assert resume_in_db.title == resume.title
    assert resume_in_db.content == resume.content


@pytest.mark.asyncio
async def test_delete_resume(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    normal_user: User,
) -> None:
    resume_data = ResumeSchema(
        title=random_lower_string(), content=random_lower_string()
    )
    await client.post(
        "/resume/", headers=normal_user_token_headers, json=resume_data.model_dump()
    )
    resume_before: Resume = (
        db.execute(select(Resume).where(Resume.user_id == normal_user.id))
        .scalars()
        .first()
    )

    r = await client.delete(
        f"/resume/{resume_before.id}", headers=normal_user_token_headers
    )
    resume_after: Resume = (
        db.execute(select(Resume).where(Resume.id == resume_before.id))
        .scalars()
        .first()
    )
    assert r.status_code == 200
    assert resume_after is None
