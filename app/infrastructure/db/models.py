from datetime import datetime, date

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .base import Base


class SchoolORM(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tax_id = Column(String(50), nullable=False, unique=True, index=True)
    address = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    students = relationship(
        "StudentORM",
        back_populates="school",
        cascade="all, delete-orphan",
    )


class StudentORM(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    grade = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    school = relationship("SchoolORM", back_populates="students")
    invoices = relationship(
        "InvoiceORM",
        back_populates="student",
        cascade="all, delete-orphan",
    )


class InvoiceORM(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    paid = Column(Boolean, default=False, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    student = relationship("StudentORM", back_populates="invoices")
