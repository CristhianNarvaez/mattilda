from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.domain.models.school import School
from app.infrastructure.db.base import SessionLocal
from app.infrastructure.repositories.student_repository_impl import (
    SqlAlchemyStudentRepository,
)
from app.infrastructure.repositories.invoice_repository_impl import (
    SqlAlchemyInvoiceRepository,
)
from app.infrastructure.repositories.school_repository_impl import (
    SqlAlchemySchoolRepository,
)
from app.schemas.school import SchoolCreate, SchoolRead, SchoolUpdate
from app.schemas.invoice import InvoiceRead
from app.services.school_service import SchoolService
from app.services.student_service import StudentService
from app.services.invoice_service import InvoiceService
from app.schemas.statement import SchoolStatement

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


@router.get(
    "/{school_id}/statement",
    response_model=SchoolStatement,
)
def get_school_statement(
    school_id: int,
    db: Session = Depends(get_db),
):
    school_repo = SqlAlchemySchoolRepository(db)
    student_repo = SqlAlchemyStudentRepository(db)
    invoice_repo = SqlAlchemyInvoiceRepository(db)

    school_service = SchoolService(school_repo)
    student_service = StudentService(student_repo)
    invoice_service = InvoiceService(invoice_repo)

    school = school_service.get_school(school_id)
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found",
        )

    students = student_service.list_students_by_school(school_id)

    all_invoices = []
    for student in students:
        student_invoices = invoice_service.list_invoices_by_student(student.id)
        all_invoices.extend(student_invoices)

    total_invoiced = sum(inv.amount for inv in all_invoices)
    total_paid = sum(inv.amount for inv in all_invoices if inv.paid)
    total_pending = total_invoiced - total_paid

    invoice_read_list = [InvoiceRead.model_validate(inv) for inv in all_invoices]

    return SchoolStatement(
        school_id=school.id,
        total_students=len(students),
        total_invoiced=total_invoiced,
        total_paid=total_paid,
        total_pending=total_pending,
        invoices=invoice_read_list,
    )
