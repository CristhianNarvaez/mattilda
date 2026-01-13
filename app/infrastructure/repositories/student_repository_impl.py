from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.models.student import Student
from app.domain.repositories.student import StudentRepository
from app.infrastructure.db.models import StudentORM


def _orm_to_domain(student_orm: StudentORM) -> Student:
    """Convert ORM object to domain model."""
    return Student(
        id=student_orm.id,
        first_name=student_orm.first_name,
        last_name=student_orm.last_name,
        email=student_orm.email,
        grade=student_orm.grade,
        is_active=student_orm.is_active,
        created_at=student_orm.created_at,
    )


class SqlAlchemyStudentRepository(StudentRepository):
    """SQLAlchemy implementation of the StudentRepository."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, student: Student) -> Student:
        obj = StudentORM(
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
            grade=student.grade,
            is_active=student.is_active,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return _orm_to_domain(obj)

    def get(self, student_id: int) -> Optional[Student]:
        obj = self.db.query(StudentORM).filter(StudentORM.id == student_id).first()
        return _orm_to_domain(obj) if obj else None

    def list(self) -> List[Student]:
        objs = self.db.query(StudentORM).all()
        return [_orm_to_domain(o) for o in objs]

    def update(self, student_id: int, student: Student) -> Optional[Student]:
        obj = self.db.query(StudentORM).filter(StudentORM.id == student_id).first()
        if not obj:
            return None

        obj.first_name = student.first_name
        obj.last_name = student.last_name
        obj.email = student.email
        obj.grade = student.grade
        obj.is_active = student.is_active

        self.db.commit()
        self.db.refresh(obj)
        return _orm_to_domain(obj)

    def delete(self, student_id: int) -> bool:
        obj = self.db.query(StudentORM).filter(StudentORM.id == student_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
