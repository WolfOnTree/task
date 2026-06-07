import csv
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException, Query, UploadFile, File

from service.autchservice import AuthService, get_auth_service
from service.studentservice import get_student_service, StudentService
from schemas.studentschema import StudentCreate, StudentUpdate, StudentInDB
from model.subjects import Faculty, Course

router = APIRouter()

@router.post(
    "/import",
    response_model=list[StudentInDB],
    status_code=status.HTTP_201_CREATED,
    summary="create_by_csv_file",
)
async def create_many(
    file: UploadFile = File(...),
    service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(text.splitlines())
    students = []
    for row in reader:
        student = StudentCreate(
            surname=row["Фамилия"],
            first_name=row["Имя"],
            faculty=Faculty(row["Факультет"]),
            course=Course(row["Курс"]),
            grade=int(row["Оценка"]),
        )
        students.append(student)

    created_students = await service.create_many(students)

    return created_students

@router.get(
    "/faculty",
    response_model=list[StudentInDB],
    status_code=status.HTTP_200_OK,
    summary="get_students_by_faculty",
)
async def get_students(
    faculty: Faculty, service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    result = await service.get_by_faculty(faculty)

    return result

@router.get(
    "/courses",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
    summary="get_all_courses",
)
async def get_courses(
    service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    result = service.get_all_courses()

    return result

@router.get(
    "/students_by_course",
    response_model=list[StudentInDB],
    status_code=status.HTTP_200_OK,
    summary="get_students_by_course_and_mark_below_30",
)
async def get_students(
    course: Course, service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    result = await service.get_by_course_and_mark_below_30(course)

    return result

@router.get(
    "/course",
    response_model=float,
    status_code=status.HTTP_200_OK,
    summary="average_grade_for_course",
)
async def get_mark(
    course: Course, service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    result = await service.get_average_mark_by_course(course)

    return result

@router.post("/", 
            response_model=StudentInDB,
            status_code=status.HTTP_201_CREATED,
            summary="create new student",
)
async def create_student(
    student_data: StudentCreate, service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    result = await service.create(student_data)
    
    return result

@router.get("/",
            response_model=list[StudentInDB],
            status_code=status.HTTP_200_OK,
            summary="get_all_students",
)
async def get_all_students(
    skip: int = Query(0, ge=0, description="offset"),
    limit: int = Query(100, ge=1, le=1000, description="limit"),
    service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    students = await service.get_all(skip, limit)

    if students is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="students table is empty")

    return students

@router.get(
    "/{student_id}",
    response_model=StudentInDB,
    status_code=status.HTTP_200_OK,
    summary="get student by id"
)
async def get_student_by_id(
    student_id: UUID, service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    student = await service.get_by_id(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"student with id: {student_id} not found")
    
    return student

@router.patch(
    "/{student_id}",
    response_model=StudentInDB,
    status_code=status.HTTP_202_ACCEPTED,
    summary="update student",
)
async def update_student(
    student_id: UUID, student_data: StudentUpdate, service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    student = await service.get_by_id(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"student with id: {student_id} not found")
    
    res = await service.update(student_id, student_data)

    return res

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="delete student")
async def delete_student(
    student_id: UUID, service: StudentService = Depends(get_student_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    auth_service.get_curent_user()

    return await service.delete(student_id)


