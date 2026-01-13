from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.student import Student


class StudentRepository(ABC):

    @abstractmethod
    def create(self, student: Student) -> Student:
        raise NotImplementedError

    @abstractmethod
    def get(self, student_id: int) -> Optional[Student]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Student]:
        raise NotImplementedError

    @abstractmethod
    def list_by_school(self, school_id: int) -> List[Student]:
        """Return all students that belong to a given school."""
        raise NotImplementedError

    @abstractmethod
    def update(self, student_id: int, student: Student) -> Optional[Student]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, student_id: int) -> bool:
        raise NotImplementedError
