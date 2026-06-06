from typing import Optional, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from model.subjects import Student, Course, Faculty
from database import get_session

class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    #базовый CRUD
    async def create(self, student_data: dict) -> Student:
        student = Student(**student_data)
        self.db.add(student)
        await self.db.commit()

        return student
    
    async def get_by_id(self, student_id: Any) -> Optional[Student]:

        result = await self.db.execute(select(Student).where(Student.id == student_id))
        return result.scalar_one_or_none()
    
    async def update(self, student_id: Any, update_data: dict):
        student = await self.get_by_id(student_id)

        if not student:
            return None
        
        for key, value in update_data.items():
            setattr(student, key, value)

        await self.db.commit()

        return student
    
    async def delete(self, student_id: Any) -> bool:
        student = await self.get_by_id(student_id)
        if student:
            await self.db.delete(student)
            await self.db.commit()
            return True
        return False
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Student]:
        result = await self.db.execute(select(Student).offset(skip).limit(limit))
        return result.scalars().all()
    #доп CRUD
    async def create_many(self, students: list[dict]) -> list[Student]:
        created_students = []
        for student in students:
            created = await self.create(student)
            created_students.append(created)

        return created_students

    async def get_by_course(self, course: Course) -> list[Student]:
        result = await self.db.execute(select(Student).where(Student.course == course.name))
        return result.scalars().all()
    
    async def get_by_faculty(self, faculty: Faculty) -> list[Student]:
        result = await self.db.execute(select(Student).where(Student.faculty == faculty.name))
        return result.scalars().all()
    
    async def get_by_course_and_mark_below_30(self, course: Course) -> list[Student]:
        result = await self.db.execute(select(Student).where(and_(Student.course == course.name, Student.grade < 30)))
        return result.scalars().all()
    
async def get_student_repo(db: AsyncSession = Depends(get_session)) -> StudentRepository:
        return StudentRepository(db)