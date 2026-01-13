from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.invoice import Invoice


class InvoiceRepository(ABC):

    @abstractmethod
    def create(self, invoice: Invoice) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    def get(self, invoice_id: int) -> Optional[Invoice]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Invoice]:
        raise NotImplementedError

    @abstractmethod
    def list_by_student(self, student_id: int) -> List[Invoice]:
        raise NotImplementedError

    @abstractmethod
    def update(self, invoice_id: int, invoice: Invoice) -> Optional[Invoice]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, invoice_id: int) -> bool:
        raise NotImplementedError
