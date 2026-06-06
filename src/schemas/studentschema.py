from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict

from model.subjects import Course, Faculty

class StudentBase(BaseModel):
    surname: str
    first_name: str
    faculty: Faculty
    course: Course
    grade: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    surname: Optional[str] = None
    first_name: Optional[str] = None
    faculty: Optional[Faculty] = None
    course: Optional[Course] = None
    grade: Optional[int] = None

class StudentInDB(StudentBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)