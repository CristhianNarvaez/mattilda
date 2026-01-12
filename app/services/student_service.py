from typing import List, Optional

from app.domain.models import student
from app.domain.repositories import student as student_repostory


class StudentService:
    """Application service for student.Student-related use cases."""

    def __init__(self, repository: student_repostory.StudentRepository) -> None:
        self.repository = repository

    def create_student(self, student: student.Student) -> student.Student:
        return self.repository.create(student)

    def get_student(self, student_id: int) -> Optional[student.Student]:
        return self.repository.get(student_id)

    def list_students(self) -> List[student.Student]:
        return self.repository.list()

    def update_student(self, student_id: int, student: student.Student) -> Optional[student.Student]:
        return self.repository.update(student_id, student)

    def delete_student(self, student_id: int) -> bool:
        return self.repository.delete(student_id)
