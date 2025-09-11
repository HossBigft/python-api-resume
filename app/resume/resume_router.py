import uuid

from fastapi import APIRouter, HTTPException
from typing import Sequence, List

from app.core.dependencies import CurrentUser, SessionDep
from app.resume.resume_shemas import ResumeIn, ResumeOut, ResumeListItemOut
from app.db.crud import (
    create_resume,
    delete_resume,
    get_resume_by_id,
    get_resume_list_by_user,
)
from app.db.models import Resume

router = APIRouter(tags=["resume"], prefix="/resume")


@router.post("/")
async def add_resume(
    session: SessionDep, resume: ResumeIn, current_user: CurrentUser
) -> str:
    create_resume(session=session, resume=resume, user_id=current_user.id)
    return "Resume added successfully"


@router.delete("/{resume_id}")
async def delete_resume_endpoint(
    session: SessionDep, resume_id: uuid.UUID, current_user: CurrentUser
) -> str:
    delete_resume(session=session, resume_id=resume_id, user_id=current_user.id)
    return "Resume deleted successfully"


@router.get("/{resume_id}")
async def get_resume_by_id_endpoint(
    session: SessionDep, resume_id: uuid.UUID, current_user: CurrentUser
) -> ResumeOut:
    resume: Resume | None = get_resume_by_id(
        session=session, resume_id=resume_id, user_id=current_user.id
    )
    if not resume:
        raise HTTPException(status_code=404, detail="Resume was not found")
    return ResumeOut.model_validate(resume)


@router.get("/")
async def get_my_resume(
    session: SessionDep, current_user: CurrentUser
) -> List[ResumeListItemOut]:
    resumes: Sequence[Resume] | None = get_resume_list_by_user(
        session=session, user_id=current_user.id
    )
    if not resumes:
        raise HTTPException(status_code=404, detail="There are no resume yet")
    return [ResumeListItemOut.model_validate(resume) for resume in resumes]
