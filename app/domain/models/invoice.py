from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class Invoice:
    id: Optional[int]
    student_id: int
    amount: float
    due_date: date
    paid: bool = False
    issued_at: Optional[datetime] = None
