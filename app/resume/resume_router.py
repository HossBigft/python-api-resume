from fastapi import APIRouter
from app.core.dependencies import CurrentUser, SessionDep
from app.resume.resume_shemas import ResumeSchema
from app.db.crud import create_resume

router = APIRouter(tags=["resume"], prefix="/resume")


@router.post("/")
def add_resume(
    session: SessionDep, resume: ResumeSchema, current_user: CurrentUser
) -> str:
    create_resume(session=session, resume=resume, db_user=current_user)
    return "Resume added successfully"


