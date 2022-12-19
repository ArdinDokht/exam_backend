from typing import Optional

from pydantic import BaseModel, validator, root_validator

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
    title_grades: Optional[str]
    grades: list[GradeWithParent]
    topics: list[Topic]

    @root_validator
    def update_title_grades(cls, values):
        grades = values.get('grades')
        if grades:
            if len(grades) == 1 and not grades[0].parent:
                values['title_grades'] = str(grades[0].title + ' ' + grades[0].base_grade.value)
            else:
                values['title_grades'] = str(grades[0].parent.title + ' ' + grades[0].parent.base_grade.value)
                values['title_grades'] += f' ({",".join(g.title for g in grades)})'
        return values

    class Config:
        orm_mode = True
