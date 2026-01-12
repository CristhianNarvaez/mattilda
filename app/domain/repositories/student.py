from abc import ABC, abstractmethod
from typing import List, Optional

from models import student


class StudentRepository(ABC):

    @abstractmethod
    def create(self, student: student.Student) -> student.Student:
        raise NotImplementedError

    @abstractmethod
    def get(self, student_id: int) -> Optional[student.Student]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[student.Student]:
        raise NotImplementedError

    @abstractmethod
    def update(self, student_id: int, student: student.Student) -> Optional[student.Student]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, student_id: int) -> bool:
        raise NotImplementedError
