from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import crud


from tests.utils.utils import random_lower_string, create_random_user
from app.db.models import Resume, User
from app.resume.resume_shemas import ResumeSchema
from app.schemas import UserPublic

def test_create_resume(db: Session) -> None:
    resume_title: str = random_lower_string()
    resume_content: str = random_lower_string()
    resume_schema: ResumeSchema = ResumeSchema(
        title=resume_title, content=resume_content
    )
    user: User = create_random_user(db)
    crud.create_resume(session=db, resume=resume_schema, user=UserPublic.model_validate(user, from_attributes=True))

    resume_in_db: Resume = (
        db.execute(select(Resume).where(Resume.user_id == user.id)).scalars().first()
    )
    assert user.id == resume_in_db.user_id
    assert resume_in_db.title == resume_title
    assert resume_in_db.content == resume_content
