from pydantic import BaseModel

from app.enums.education_system import BaseGrade


class Grade(BaseModel):
    id: int
    title: str
    base_grade: BaseGrade
    children: list['Grade']

    class Config:
        orm_mode = True
