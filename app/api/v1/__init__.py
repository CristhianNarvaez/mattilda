from .students import router as students_router
from .invoices import router as invoices_router

__all__ = [
    "students_router",
    "invoices_router",
]
