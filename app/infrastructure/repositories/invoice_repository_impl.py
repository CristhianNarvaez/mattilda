from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.models import invoice
from app.domain.repositories import InvoiceRepository
from app.infrastructure.db.models import InvoiceORM


def _orm_to_domain(invoice_orm: InvoiceORM) -> invoice.Invoice:
    """Convert ORM object to domain model."""
    return invoice.Invoice(
        id=invoice_orm.id,
        student_id=invoice_orm.student_id,
        amount=invoice_orm.amount,
        due_date=invoice_orm.due_date,
        paid=invoice_orm.paid,
        issued_at=invoice_orm.issued_at,
    )


class SqlAlchemyInvoiceRepository(InvoiceRepository):
    """SQLAlchemy implementation of the InvoiceRepository."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, invoice: invoice.Invoice) -> invoice.Invoice:
        obj = InvoiceORM(
            student_id=invoice.student_id,
            amount=invoice.amount,
            due_date=invoice.due_date,
            paid=invoice.paid,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return _orm_to_domain(obj)

    def get(self, invoice_id: int) -> Optional[invoice.Invoice]:
        obj = self.db.query(InvoiceORM).filter(InvoiceORM.id == invoice_id).first()
        return _orm_to_domain(obj) if obj else None

    def list(self) -> List[invoice.Invoice]:
        objs = self.db.query(InvoiceORM).all()
        return [_orm_to_domain(o) for o in objs]

    def list_by_student(self, student_id: int) -> List[invoice.Invoice]:
        objs = (
            self.db.query(InvoiceORM).filter(InvoiceORM.student_id == student_id).all()
        )
        return [_orm_to_domain(o) for o in objs]

    def update(self, invoice_id: int, invoice: invoice.Invoice) -> Optional[invoice.Invoice]:
        obj = self.db.query(InvoiceORM).filter(InvoiceORM.id == invoice_id).first()
        if not obj:
            return None

        obj.student_id = invoice.student_id
        obj.amount = invoice.amount
        obj.due_date = invoice.due_date
        obj.paid = invoice.paid

        self.db.commit()
        self.db.refresh(obj)
        return _orm_to_domain(obj)

    def delete(self, invoice_id: int) -> bool:
        obj = self.db.query(InvoiceORM).filter(InvoiceORM.id == invoice_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
