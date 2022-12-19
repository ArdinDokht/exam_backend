from typing import Optional

from pydantic import BaseModel, root_validator

from app import enums


class GradeBase(BaseModel):
    title: str
    base_grade: enums.BaseGrade

    class Config:
        orm_mode = True


class GradeCreate(GradeBase):
    pass


class GradeUpdate(GradeBase):
    pass


class GradeWithParent(GradeBase):
    id: int
    full_title: Optional[str]
    parent: Optional[GradeBase]

    @root_validator
    def update_full_title(cls, values):
        if not values.get('parent'):
            values['full_title'] = values['title'] + ' ' + values['base_grade'].value
        else:
            values['full_title'] = f'{values["parent"].title} {values["base_grade"].value} ({values["title"]})'

        return values


class Grade(GradeBase):
    id: int
    children: list['Grade']

    class Config:
        orm_mode = True
