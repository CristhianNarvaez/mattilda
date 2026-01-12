from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Student:
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    grade: str
    is_active: bool = True
    created_at: Optional[datetime] = None
