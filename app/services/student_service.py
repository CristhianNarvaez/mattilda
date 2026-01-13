from typing import List, Optional

from app.domain.models.student import Student
from app.domain.repositories import student as student_repostory


class StudentService:
    """Application service for Student-related use cases."""

    def __init__(self, repository: student_repostory.StudentRepository) -> None:
        self.repository = repository

    def create_student(self, student: Student) -> Student:
        return self.repository.create(student)

    def get_student(self, student_id: int) -> Optional[Student]:
        return self.repository.get(student_id)

    def list_students(self) -> List[Student]:
        return self.repository.list()

    def list_students_by_school(self, school_id: int) -> List[Student]:
        return self.repository.list_by_school(school_id)

    def update_student(self, student_id: int, student: Student) -> Optional[Student]:
        return self.repository.update(student_id, student)

    def delete_student(self, student_id: int) -> bool:
        return self.repository.delete(student_id)
