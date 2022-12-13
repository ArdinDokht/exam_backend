from typing import Optional

from pydantic import BaseModel

from app.schemas.education_system import GradeWithParent


# ---------------- topic schemas -------------------- #

class Topic(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


# ---------------- lesson schemas -------------------- #
# class LessonBase(BaseModel):
#     title: str


class LessonCreate(BaseModel):
    title: str


class LessonUpdate(BaseModel):
    title: str


class LessonSimple(BaseModel):
    id: int
    title: str
    grades: list[GradeWithParent]

    class Config:
        orm_mode = True


class Lesson(BaseModel):
    id: int
    title: str
    # title_grades: Optional[str]
    grades: list[GradeWithParent]
    topics: list[Topic]

    class Config:
        orm_mode = True
