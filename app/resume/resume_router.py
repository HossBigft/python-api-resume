import uuid

from fastapi import APIRouter


from app.core.dependencies import CurrentUser, SessionDep
from app.resume.resume_shemas import ResumeSchema
from app.db.crud import create_resume, delete_resume

router = APIRouter(tags=["resume"], prefix="/resume")


@router.post("/")
async def add_resume(
    session: SessionDep, resume: ResumeSchema, current_user: CurrentUser
) -> str:
    create_resume(session=session, resume=resume, db_user=current_user)
    return "Resume added successfully"


@router.delete("/{resume_id}")
async def delete_resume_endpoint(
    session: SessionDep, resume_id: uuid.UUID, current_user: CurrentUser
) -> str:
    delete_resume(session=session, resume_id=resume_id, db_user=current_user)
    return "Resume deleted successfully"