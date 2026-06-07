import uuid
from enum import Enum

from sqlalchemy import Column, String, Boolean, Integer, Enum as SQLEnum
from .base import Base, BaseModelMixin

class User(Base, BaseModelMixin):

    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Faculty(Enum):
    AVTF = 'АВТФ'
    FPMI = 'ФПМИ'
    FLA = 'ФЛА'
    REF = 'РЭФ'
    FTF ='ФТФ'

class Course(Enum):
    Theor_Mechanics = 'Теор. Механика'
    Mat_Analysis = 'Мат. Анализ'
    Informatics = 'Информатика'
    History = 'История'
    Psychology = 'Психология'
    Physics = 'Физика'


class Student(Base, BaseModelMixin):

    __tablename__ = "students"

    surname = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    faculty = Column(SQLEnum(Faculty), nullable=False)
    course = Column(SQLEnum(Course), nullable=False)
    grade = Column(Integer, default=0)