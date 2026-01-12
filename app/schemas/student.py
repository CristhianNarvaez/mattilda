from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    grade: str
    is_active: bool = True


class StudentCreate(StudentBase):
    """Payload used when creating a new student."""

    pass


class StudentUpdate(StudentBase):
    """Payload used when updating an existing student."""

    pass


class StudentRead(StudentBase):
    """Representation of a student returned by the API."""

    id: int
    created_at: datetime

    class Config:
        orm_mode = True
