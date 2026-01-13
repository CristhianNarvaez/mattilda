from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.models.school import School


class SchoolRepository(ABC):

    @abstractmethod
    def create(self, school: School) -> School:
        raise NotImplementedError

    @abstractmethod
    def get(self, school_id: int) -> Optional[School]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[School]:
        raise NotImplementedError

    @abstractmethod
    def update(self, school_id: int, school: School) -> Optional[School]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, school_id: int) -> bool:
        raise NotImplementedError
