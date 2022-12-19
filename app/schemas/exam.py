import datetime

from pydantic import BaseModel

from app import enums
from app.schemas.education_system import GradeWithParent


class ExamBase(BaseModel):
    title: str
    type: enums.ExamType
    start_datetime: datetime.datetime
    duration: int


class ExamCreate(ExamBase):
    grade_id: int


class ExamUpdate(ExamBase):
    pass


class Exam(ExamBase):
    id: int
    grade: GradeWithParent

    class Config:
        orm_mode = True
