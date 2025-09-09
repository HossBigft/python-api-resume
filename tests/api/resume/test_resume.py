import pytest

from httpx import AsyncClient
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.resume.resume_shemas import ResumeSchema
from tests.utils.utils import random_lower_string
from app.db.models import Resume, User


@pytest.mark.asyncio
async def test_create_resume(
    client: AsyncClient, normal_user_token_headers: dict[str, str], db: Session, normal_user: User
) -> None:
    resume = ResumeSchema(title=random_lower_string(), content=random_lower_string())
    response =await client.post(
        "/resume/", headers=normal_user_token_headers, json=resume.model_dump()
    )
    resume_in_db: Resume = (
        db.execute(select(Resume).where(Resume.user_id == normal_user.id)).scalars().first()
    )
    assert resume_in_db.title == resume.title
    assert resume_in_db.content == resume.content

    