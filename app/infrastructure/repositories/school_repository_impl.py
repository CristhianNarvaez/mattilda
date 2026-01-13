from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.models.school import School
from app.domain.repositories.school import SchoolRepository
from app.infrastructure.db.models import SchoolORM


def _orm_to_domain(school_orm: SchoolORM) -> School:
    return School(
        id=school_orm.id,
        name=school_orm.name,
        tax_id=school_orm.tax_id,
        address=school_orm.address,
        is_active=school_orm.is_active,
        created_at=school_orm.created_at,
    )


class SqlAlchemySchoolRepository(SchoolRepository):
    """SQLAlchemy implementation of the SchoolRepository."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, school: School) -> School:
        obj = SchoolORM(
            name=school.name,
            tax_id=school.tax_id,
            address=school.address,
            is_active=school.is_active,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return _orm_to_domain(obj)

    def get(self, school_id: int) -> Optional[School]:
        obj = self.db.query(SchoolORM).filter(SchoolORM.id == school_id).first()
        return _orm_to_domain(obj) if obj else None

    def list(self) -> List[School]:
        objs = self.db.query(SchoolORM).all()
        return [_orm_to_domain(o) for o in objs]

    def update(self, school_id: int, school: School) -> Optional[School]:
        obj = self.db.query(SchoolORM).filter(SchoolORM.id == school_id).first()
        if not obj:
            return None

        obj.name = school.name
        obj.tax_id = school.tax_id
        obj.address = school.address
        obj.is_active = school.is_active

        self.db.commit()
        self.db.refresh(obj)
        return _orm_to_domain(obj)

    def delete(self, school_id: int) -> bool:
        obj = self.db.query(SchoolORM).filter(SchoolORM.id == school_id).first()
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
