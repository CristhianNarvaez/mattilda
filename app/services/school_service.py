from typing import List, Optional

from app.domain.models.school import School
from app.domain.repositories.school import SchoolRepository


class SchoolService:
    """Application service for school-related use cases."""

    def __init__(self, repository: SchoolRepository) -> None:
        self.repository = repository

    def create_school(self, school: School) -> School:
        return self.repository.create(school)

    def get_school(self, school_id: int) -> Optional[School]:
        return self.repository.get(school_id)

    def list_schools(self) -> List[School]:
        return self.repository.list()

    def update_school(self, school_id: int, school: School) -> Optional[School]:
        return self.repository.update(school_id, school)

    def delete_school(self, school_id: int) -> bool:
        return self.repository.delete(school_id)
