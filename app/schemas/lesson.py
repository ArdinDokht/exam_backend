from typing import Optional

from pydantic import BaseModel

from app.schemas.education_system import SimpleGrade


# ---------------- lesson parent schemas -------------------- #
class LessonParentBase(BaseModel):
    title: str


class LessonParentCreate(LessonParentBase):
    pass


class LessonParentUpdate(LessonParentBase):
    pass


class LessonParent(LessonParentBase):
    id: int

    class Config:
        orm_mode = True


# ---------------- lesson schemas -------------------- #
class LessonBase(BaseModel):
    lesson_parent_id: int
    grade_id: int


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class Lesson(BaseModel):
    id: int
    title: Optional[str]
    lesson_parent: LessonParent
    grade: SimpleGrade

    class Config:
        orm_mode = True
