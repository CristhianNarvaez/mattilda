from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class School:
    id: Optional[int]
    name: str
    tax_id: str
    address: str
    is_active: bool = True
    created_at: Optional[datetime] = None
