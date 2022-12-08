from pydantic import BaseModel

from app import enums


class GradeBase(BaseModel):
    title: str
    base_grade: enums.BaseGrade


class GradeCreate(GradeBase):
    pass


class GradeUpdate(GradeBase):
    pass


class Grade(GradeBase):
    id: int
    children: list['Grade']

    class Config:
        orm_mode = True
