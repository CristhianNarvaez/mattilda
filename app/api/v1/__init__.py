from .students import router as students_router
from .invoices import router as invoices_router
from .schools import router as schools_router

__all__ = [
    "students_router",
    "invoices_router",
    "schools_router",
]
