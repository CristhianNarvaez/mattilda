from typing import List

from pydantic import BaseModel

from app.schemas.invoice import InvoiceRead


class StudentStatement(BaseModel):
    student_id: int
    school_id: int
    total_invoiced: float
    total_paid: float
    total_pending: float
    invoices: List[InvoiceRead]


class SchoolStatement(BaseModel):
    school_id: int
    total_students: int
    total_invoiced: float
    total_paid: float
    total_pending: float
    invoices: List[InvoiceRead]
