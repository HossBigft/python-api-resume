from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import crud


from tests.utils.utils import random_lower_string
from app.db.models import Resume, User
from app.resume.resume_shemas import ResumeIn


def test_create_resume(db: Session, normal_user: User) -> None:
    resume_title: str = random_lower_string()
    resume_content: str = random_lower_string()
    resume_schema: ResumeIn = ResumeIn(
        title=resume_title, content=resume_content
    )
    crud.create_resume(
        session=db,
        resume=resume_schema,
        db_user=normal_user,
    )

    resume_in_db: Resume = (
        db.execute(select(Resume).where(Resume.user_id == normal_user.id))
        .scalars()
        .first()
    )
    assert normal_user.id == resume_in_db.user_id
    assert resume_in_db.title == resume_title
    assert resume_in_db.content == resume_content


def test_delete_resume(db: Session, normal_user: User) -> None:
    resume_title: str = random_lower_string()
    resume_content: str = random_lower_string()
    resume_schema: ResumeIn = ResumeIn(
        title=resume_title, content=resume_content
    )

    resume = crud.create_resume(
        session=db,
        resume=resume_schema,
        db_user=normal_user,
    )

    crud.delete_resume(session=db, resume_id=resume.id, db_user=normal_user)
    resume_in_db: Resume = (
        db.execute(select(Resume).where(Resume == resume)).scalars().first()
    )
    assert resume_in_db is None


def test_get_resume(db: Session, normal_user: User) -> None:
    resume_title: str = random_lower_string()
    resume_content: str = random_lower_string()
    resume_schema: ResumeIn = ResumeIn(
        title=resume_title, content=resume_content
    )

    created_resume: Resume | None = crud.create_resume(
        session=db,
        resume=resume_schema,
        db_user=normal_user,
    )
    assert created_resume is not None

    received_in_db: Resume | None = crud.get_resume_by_id(
        session=db, resume_id=created_resume.id, db_user=normal_user
    )

    assert received_in_db is not None
    assert created_resume.id==received_in_db.id
