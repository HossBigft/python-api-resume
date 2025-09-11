import pytest

from httpx import AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.resume.resume_shemas import ResumeIn, ResumeOut, ResumeListItemOut
from tests.utils.utils import random_lower_string
from app.db.models import Resume, User


@pytest.mark.asyncio
async def test_create_resume(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    normal_user: User,
) -> None:
    resume = ResumeIn(title=random_lower_string(), content=random_lower_string())
    await client.post(
        "/resume/", headers=normal_user_token_headers, json=resume.model_dump()
    )
    resume_in_db: Resume | None = (
        db.execute(select(Resume).where(Resume.user_id == normal_user.id))
        .scalars()
        .first()
    )
    assert resume_in_db is not None
    assert resume_in_db.title == resume.title
    assert resume_in_db.content == resume.content


@pytest.mark.asyncio
async def test_delete_resume(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    normal_user: User,
) -> None:
    resume_data = ResumeIn(title=random_lower_string(), content=random_lower_string())
    await client.post(
        "/resume/", headers=normal_user_token_headers, json=resume_data.model_dump()
    )
    resume_before: Resume | None = (
        db.execute(select(Resume).where(Resume.user_id == normal_user.id))
        .scalars()
        .first()
    )
    assert resume_before is not None

    r = await client.delete(
        f"/resume/{resume_before.id}", headers=normal_user_token_headers
    )
    resume_after: Resume | None = (
        db.execute(select(Resume).where(Resume.id == resume_before.id))
        .scalars()
        .first()
    )
    assert r.status_code == 200
    assert resume_after is None


@pytest.mark.asyncio
async def test_get_resume(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    normal_user: User,
) -> None:
    resume_data = ResumeIn(title=random_lower_string(), content=random_lower_string())
    await client.post(
        "/resume/", headers=normal_user_token_headers, json=resume_data.model_dump()
    )
    resume_via_crud: Resume | None = (
        db.execute(select(Resume).where(Resume.user_id == normal_user.id))
        .scalars()
        .first()
    )
    assert resume_via_crud is not None

    r = await client.get(
        f"/resume/{resume_via_crud.id}", headers=normal_user_token_headers
    )

    resume_via_api: ResumeOut = ResumeOut.model_validate(r.json())
    assert r.status_code == 200
    assert resume_via_crud.id == resume_via_api.id
    assert resume_via_crud.title == resume_via_api.title
    assert resume_via_crud.content == resume_via_api.content


@pytest.mark.asyncio
async def test_get_resume_by_user(
    client: AsyncClient,
    normal_user_token_headers: dict[str, str]
) -> None:
    for i in range(0, 3):
        resume_data = ResumeIn(
            title=random_lower_string(), content=random_lower_string()
        )
        await client.post(
            "/resume/", headers=normal_user_token_headers, json=resume_data.model_dump()
        )

    r = await client.get("/resume/", headers=normal_user_token_headers)
    print("RESPONSE_R", r.json())
    resume_via_api: List[ResumeListItemOut] = [
        ResumeListItemOut.model_validate(resume) for resume in r.json()
    ]
    assert r.status_code == 200
    assert len(resume_via_api) == 3
