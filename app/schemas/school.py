from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SchoolBase(BaseModel):
    name: str
    tax_id: str
    address: str
    is_active: bool = True


class SchoolCreate(SchoolBase):
    """Payload used when creating a new school."""

    pass


class SchoolUpdate(SchoolBase):
    """Payload used when updating an existing school."""

    pass


class SchoolRead(SchoolBase):
    """School representation returned by the API."""

    id: int
    created_at: datetime

    class Config:
        orm_mode = True
