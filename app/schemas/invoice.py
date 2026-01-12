from datetime import date, datetime

from pydantic import BaseModel


class InvoiceBase(BaseModel):
    student_id: int
    amount: float
    due_date: date
    paid: bool = False


class InvoiceCreate(InvoiceBase):
    """Payload used when creating a new invoice."""

    pass


class InvoiceUpdate(InvoiceBase):
    """Payload used when updating an existing invoice."""

    pass


class InvoiceRead(InvoiceBase):
    """Representation of an invoice returned by the API."""

    id: int
    issued_at: datetime

    class Config:
        orm_mode = True
