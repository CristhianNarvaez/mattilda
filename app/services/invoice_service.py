from typing import List, Optional

from app.domain.models.invoice import Invoice
from app.domain.repositories import invoice as invoice_repository


class InvoiceService:
    """Application service for Invoice-related use cases."""

    def __init__(self, repository: invoice_repository.InvoiceRepository) -> None:
        self.repository = repository

    def create_invoice(self, invoice: Invoice) -> Invoice:
        return self.repository.create(invoice)

    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        return self.repository.get(invoice_id)

    def list_invoices(self) -> List[Invoice]:
        return self.repository.list()

    def list_invoices_by_student(self, student_id: int) -> List[Invoice]:
        return self.repository.list_by_student(student_id)

    def update_invoice(self, invoice_id: int, invoice: Invoice) -> Optional[Invoice]:
        return self.repository.update(invoice_id, invoice)

    def delete_invoice(self, invoice_id: int) -> bool:
        return self.repository.delete(invoice_id)
