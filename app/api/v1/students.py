from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.domain.models.student import Student
from app.infrastructure.db.base import SessionLocal
from app.infrastructure.repositories.student_repository_impl import (
    SqlAlchemyStudentRepository,
)
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter(
    prefix="/students",
    tags=["students"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    repository = SqlAlchemyStudentRepository(db)
    return StudentService(repository)


@router.post(
    "/",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    payload: StudentCreate,
    service: StudentService = Depends(get_student_service),
):
    student = Student(
        id=None,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        grade=payload.grade,
        is_active=payload.is_active,
    )
    created = service.create_student(student)
    return created


@router.get(
    "/",
    response_model=List[StudentRead],
)
def list_students(
    service: StudentService = Depends(get_student_service),
):
    return service.list_students()


@router.get(
    "/{student_id}",
    response_model=StudentRead,
)
def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    student = service.get_student(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student


@router.put(
    "/{student_id}",
    response_model=StudentRead,
)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    service: StudentService = Depends(get_student_service),
):
    student = Student(
        id=student_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        grade=payload.grade,
        is_active=payload.is_active,
    )
    updated = service.update_student(student_id, student)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return updated


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    deleted = service.delete_student(student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return None
