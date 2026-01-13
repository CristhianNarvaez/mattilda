from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


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
    id: int
    issued_at: datetime

    model_config = ConfigDict(from_attributes=True)
