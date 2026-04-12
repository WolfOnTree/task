import uuid
from enum import Enum

from sqlalchemy import Column, String, Boolean, Integer, Enum as SQLEnum
from .base import Base, BaseModelMixin

class faculty(Enum):
    AVTF = 'АВТФ'
    FPMI = 'ФПМИ'
    FLA = 'ФЛА'
    REF = 'РЭФ'
    FTF ='ФТФ'

class course(Enum):
    Theor_Mechanics = 'Теор. Механика'
    Mat_Analysis = 'Мат. Анализ'
    Informatics = 'Информатика'
    History = 'История'
    Psychology = 'Психология'
    Physics = 'Физика'


class Students(Base, BaseModelMixin):

    __tablename__ = "students"

    surname = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    faculty = Column(SQLEnum(faculty), nullable=False)
    course = Column(SQLEnum(course), nullable=False)
    grade = Column(Integer, default=0)