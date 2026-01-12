from abc import ABC, abstractmethod
from typing import List, Optional

from models import invoice


class InvoiceRepository(ABC):

    @abstractmethod
    def create(self, invoice: invoice.Invoice) -> invoice.Invoice:
        raise NotImplementedError

    @abstractmethod
    def get(self, invoice_id: int) -> Optional[invoice.Invoice]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[invoice.Invoice]:
        raise NotImplementedError

    @abstractmethod
    def list_by_student(self, student_id: int) -> List[invoice.Invoice]:
        raise NotImplementedError

    @abstractmethod
    def update(self, invoice_id: int, invoice: invoice.Invoice) -> Optional[invoice.Invoice]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, invoice_id: int) -> bool:
        raise NotImplementedError
