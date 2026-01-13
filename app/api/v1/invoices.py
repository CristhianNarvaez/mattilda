from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.domain.models.invoice import Invoice
from app.infrastructure.db.base import SessionLocal
from app.infrastructure.repositories.invoice_repository_impl import (
    SqlAlchemyInvoiceRepository,
)
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate
from app.services.invoice_service import InvoiceService

router = APIRouter(
    prefix="/invoices",
    tags=["invoices"],
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_invoice_service(db: Session = Depends(get_db)) -> InvoiceService:
    repository = SqlAlchemyInvoiceRepository(db)
    return InvoiceService(repository)


@router.post(
    "/",
    response_model=InvoiceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_invoice(
    payload: InvoiceCreate,
    service: InvoiceService = Depends(get_invoice_service),
):
    invoice = Invoice(
        id=None,
        student_id=payload.student_id,
        amount=payload.amount,
        due_date=payload.due_date,
        paid=payload.paid,
    )
    created = service.create_invoice(invoice)
    return created


@router.get(
    "/",
    response_model=List[InvoiceRead],
)
def list_invoices(
    service: InvoiceService = Depends(get_invoice_service),
):
    return service.list_invoices()


@router.get(
    "/{invoice_id}",
    response_model=InvoiceRead,
)
def get_invoice(
    invoice_id: int,
    service: InvoiceService = Depends(get_invoice_service),
):
    invoice = service.get_invoice(invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    return invoice


@router.put(
    "/{invoice_id}",
    response_model=InvoiceRead,
)
def update_invoice(
    invoice_id: int,
    payload: InvoiceUpdate,
    service: InvoiceService = Depends(get_invoice_service),
):
    invoice = Invoice(
        id=invoice_id,
        student_id=payload.student_id,
        amount=payload.amount,
        due_date=payload.due_date,
        paid=payload.paid,
    )
    updated = service.update_invoice(invoice_id, invoice)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    return updated


@router.delete(
    "/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_invoice(
    invoice_id: int,
    service: InvoiceService = Depends(get_invoice_service),
):
    deleted = service.delete_invoice(invoice_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    return None
