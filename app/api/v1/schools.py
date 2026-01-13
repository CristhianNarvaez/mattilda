from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.domain.models.school import School
from app.infrastructure.db.base import SessionLocal
from app.infrastructure.repositories.school_repository_impl import (
    SqlAlchemySchoolRepository,
)
from app.schemas.school import SchoolCreate, SchoolRead, SchoolUpdate
from app.services.school_service import SchoolService

router = APIRouter(
    prefix="/schools",
    tags=["schools"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_school_service(db: Session = Depends(get_db)) -> SchoolService:
    repository = SqlAlchemySchoolRepository(db)
    return SchoolService(repository)


@router.post(
    "/",
    response_model=SchoolRead,
    status_code=status.HTTP_201_CREATED,
)
def create_school(
    payload: SchoolCreate,
    service: SchoolService = Depends(get_school_service),
):
    school = School(
        id=None,
        name=payload.name,
        tax_id=payload.tax_id,
        address=payload.address,
        is_active=payload.is_active,
    )
    created = service.create_school(school)
    return created


@router.get(
    "/",
    response_model=List[SchoolRead],
)
def list_schools(
    service: SchoolService = Depends(get_school_service),
):
    return service.list_schools()


@router.get(
    "/{school_id}",
    response_model=SchoolRead,
)
def get_school(
    school_id: int,
    service: SchoolService = Depends(get_school_service),
):
    school = service.get_school(school_id)
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found",
        )
    return school


@router.put(
    "/{school_id}",
    response_model=SchoolRead,
)
def update_school(
    school_id: int,
    payload: SchoolUpdate,
    service: SchoolService = Depends(get_school_service),
):
    school = School(
        id=school_id,
        name=payload.name,
        tax_id=payload.tax_id,
        address=payload.address,
        is_active=payload.is_active,
    )
    updated = service.update_school(school_id, school)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found",
        )
    return updated


@router.delete(
    "/{school_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_school(
    school_id: int,
    service: SchoolService = Depends(get_school_service),
):
    deleted = service.delete_school(school_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found",
        )
    return None
