from typing import Any, Optional

from fastapi import Depends

from model.subjects import Course, Faculty
from repos.studentrepo import StudentRepository, get_student_repo
from schemas.studentschema import StudentInDB, StudentCreate, StudentUpdate

class StudentService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo
    #база
    async def get_by_id(self, student_id: Any) -> StudentInDB:
        student = await self.repo.get_by_id(student_id)

        return student
    
    async def create(self, student_data: StudentCreate) -> StudentInDB:
        dict_data = student_data.model_dump()
        student = await self.repo.create(dict_data)

        return student
    
    async def update(self, student_id: Any, student_data: StudentUpdate) -> Optional[StudentInDB]:
        dict_data = {
            key: value 
            for key, value in student_data.model_dump().items()
            if value is not None 
        }

        if not dict_data:
            return None

        student = await self.repo.update(student_id, dict_data)

        return student
    
    async def delete(self, student_id: Any) -> bool:
        return await self.repo.delete(student_id)
    
    async def get_all(self, skip: int, limit: int) -> list[StudentInDB]:
        return await self.repo.get_all(skip, limit)
    #доп
    async def create_many(self, students_data: list[StudentCreate]) -> list[StudentInDB]:
        dicts_list = [studedent_data.model_dump() for studedent_data in students_data]
        return await self.repo.create_many(dicts_list)
    
    async def get_by_faculty(self, faculty: Faculty) -> list[StudentInDB]:
        return await self.repo.get_by_faculty(faculty)
    
    def get_all_courses(self) -> list[str]:
        result = [course.value for course in Course]
        return result

    async def get_by_course_and_mark_below_30(self, course: Course) -> list[StudentInDB]:
        return await self.repo.get_by_course_and_mark_below_30(course)
    
    async def get_average_mark_by_course(self, course: Course) -> int:
        studets_by_course = await self.repo.get_by_course(course)
        result = sum(student.grade for student in studets_by_course)/len(studets_by_course)

        return result

async def get_student_service(repo: StudentRepository = Depends(get_student_repo)) -> StudentService:
        return StudentService(repo)